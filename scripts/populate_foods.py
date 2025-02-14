import os
import sys
import requests
from tqdm import tqdm
from dotenv import load_dotenv

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Food

load_dotenv()

USDA_API_KEY = os.getenv('USDA_API_KEY')
USDA_API_ENDPOINT = 'https://api.nal.usda.gov/fdc/v1'
NUTRIENTS_OF_INTEREST = {
    '1008': 'calories_per_100g',    # Energy (kcal)
    '1003': 'protein_per_100g',     # Protein
    '1004': 'fat_per_100g',         # Total fat
    '1005': 'carbs_per_100g',       # Carbohydrates
}

def fetch_food_data(page_size=50, page_number=1):
    """Fetch food data from USDA API"""
    params = {
        'api_key': USDA_API_KEY,
        'pageSize': page_size,
        'pageNumber': page_number,
        'dataType': 'Foundation,SR Legacy',  # Use standard reference database
        'sortBy': 'dataType.keyword',
    }
    
    response = requests.get(f'{USDA_API_ENDPOINT}/foods/search', params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def extract_nutrient_values(food_item):
    """Extract nutrient values from a food item"""
    nutrients = {key: None for key in NUTRIENTS_OF_INTEREST.values()}
    
    if 'foodNutrients' in food_item:
        for nutrient in food_item['foodNutrients']:
            nutrient_id = str(nutrient.get('nutrientId', ''))
            if nutrient_id in NUTRIENTS_OF_INTEREST:
                key = NUTRIENTS_OF_INTEREST[nutrient_id]
                value = nutrient.get('value', 0)
                nutrients[key] = value if value is not None else 0
    
    return nutrients

def truncate_name(name, max_length=95):
    """Truncate food name and add '...' if it's too long"""
    if len(name) <= max_length:
        return name
    return name[:max_length] + '...'

def populate_database():
    """Populate database with USDA food data"""
    if not USDA_API_KEY:
        print("Error: USDA_API_KEY not found in environment variables")
        return

    app = create_app()
    with app.app_context():
        page = 1
        total_foods = 0
        
        while True:
            print(f"\nFetching page {page}...")
            data = fetch_food_data(page_size=50, page_number=page)
            
            if not data or not data.get('foods'):
                break
                
            foods = data['foods']
            if not foods:
                break
                
            for food_item in tqdm(foods, desc="Processing foods"):
                # Skip if food already exists
                if Food.query.filter_by(usda_id=str(food_item['fdcId'])).first():
                    continue
                    
                nutrients = extract_nutrient_values(food_item)
                
                # Skip if no calorie information (our only required field)
                if not nutrients['calories_per_100g']:
                    continue
                
                # Truncate food name if necessary
                truncated_name = truncate_name(food_item['description'])
                
                food = Food(
                    name=truncated_name,
                    usda_id=str(food_item['fdcId']),
                    **nutrients
                )
                
                try:
                    db.session.add(food)
                    db.session.commit()
                    total_foods += 1
                except Exception as e:
                    print(f"Error adding food {truncated_name}: {str(e)}")
                    db.session.rollback()
            
            page += 1
            print(f"\nTotal foods added: {total_foods}")
            
            # Stop after processing 1000 foods (20 pages) - adjust as needed
            if page > 20:
                break

if __name__ == '__main__':
    populate_database()