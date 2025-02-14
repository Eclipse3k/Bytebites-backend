import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Food
from config import TestingConfig

def verify_database():
    """Verify the foods in the database"""
    app = create_app(TestingConfig)
    
    with app.app_context():
        # Get total count
        total_foods = Food.query.count()
        print(f"\nTotal foods in database: {total_foods}")
        
        if total_foods == 0:
            print("No foods found in database!")
            return
            
        # Show some sample entries
        print("\nSample entries:")
        sample_foods = Food.query.limit(5).all()
        for food in sample_foods:
            print(f"\nName: {food.name}")
            print(f"Calories per 100g: {food.calories_per_100g}")
            print(f"Protein per 100g: {food.protein_per_100g}")
            print(f"Carbs per 100g: {food.carbs_per_100g}")
            print(f"Fat per 100g: {food.fat_per_100g}")
            print(f"USDA ID: {food.usda_id}")
            
        # Show nutrient coverage
        foods_with_protein = Food.query.filter(Food.protein_per_100g.isnot(None)).count()
        foods_with_carbs = Food.query.filter(Food.carbs_per_100g.isnot(None)).count()
        foods_with_fat = Food.query.filter(Food.fat_per_100g.isnot(None)).count()
        
        print(f"\nNutrient coverage:")
        print(f"Foods with protein data: {foods_with_protein}/{total_foods}")
        print(f"Foods with carbs data: {foods_with_carbs}/{total_foods}")
        print(f"Foods with fat data: {foods_with_fat}/{total_foods}")

if __name__ == '__main__':
    verify_database()