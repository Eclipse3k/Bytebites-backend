import pytest
from app import create_app, db
from app.models import User, Food, FoodLog
from config import TestingConfig

@pytest.fixture
def app():
    """Fixture to create the test app and database tables."""
    app = create_app(TestingConfig)
    
    with app.app_context():
        # Print current database URI
        print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        # Drop all tables first to ensure clean state
        print("Dropping existing tables...")
        db.drop_all()
        
        # Create tables
        print("Creating database tables...")
        db.create_all()
        
        # Verify tables
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Created tables: {tables}")
        
        yield app
        
        print("Cleaning up...")
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture
def register_and_login(client):
    """Helper fixture to register and log in a user."""
    # Register the user
    client.post('/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    # Log in the user and get the token 
    response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    return data['access_token']

def test_create_food(client, register_and_login):
    """Test creating a custom food item."""
    headers = {'Authorization': f'Bearer {register_and_login}'}
    
    # Test successful food creation
    food_data = {
        'name': 'Custom Pizza',
        'calories_per_100g': 267.0,
        'protein_per_100g': 11.0,
        'carbs_per_100g': 33.0,
        'fat_per_100g': 9.8
    }
    
    response = client.post('/foods', json=food_data, headers=headers)
    assert response.status_code == 201
    assert 'Food created successfully' in response.get_json()['message']
    
    # Test duplicate food name
    response = client.post('/foods', json=food_data, headers=headers)
    assert response.status_code == 400
    assert 'already exists' in response.get_json()['message']
    
    # Test missing required fields
    incomplete_data = {'name': 'Incomplete Food'}
    response = client.post('/foods', json=incomplete_data, headers=headers)
    assert response.status_code == 400
    assert 'required' in response.get_json()['message']

def test_add_food_log(client, register_and_login):
    """Test creating a food log for a user."""
    food = Food(name="Apple", calories_per_100g=52.0, protein_per_100g=0.3, carbs_per_100g=14.0, fat_per_100g=0.2)
    db.session.add(food)
    db.session.commit()

    # Get the user first
    user = User.query.filter_by(username='testuser').first()

    food_log_data = {
        'food_id': food.id,
        'grams': 150
    }

    headers = {
        'Authorization': f'Bearer {register_and_login}'
    }

    response = client.post('/food_logs', json=food_log_data, headers=headers)
    
    if response.status_code != 201:
        print("Error response:", response.get_json())
        
    assert response.status_code == 201
    assert b'Food log created successfully' in response.data

    food_log = FoodLog.query.filter_by(user_id=user.id, food_id=food.id).first()
    assert food_log is not None
    assert food_log.grams == 150
    assert food_log.food.name == "Apple"

def test_add_food_log_complete_workflow(client, register_and_login):
    """Test the complete workflow of creating a food and logging it."""
    headers = {'Authorization': f'Bearer {register_and_login}'}
    
    # First create a custom food
    food_data = {
        'name': 'Homemade Cookies',
        'calories_per_100g': 450.0,
        'protein_per_100g': 5.0,
        'carbs_per_100g': 67.0,
        'fat_per_100g': 21.0
    }
    
    response = client.post('/foods', json=food_data, headers=headers)
    assert response.status_code == 201
    food_id = response.get_json()['food']['id']
    
    # Now log this food
    food_log_data = {
        'food_id': food_id,
        'grams': 50  # logging 50g of cookies
    }
    
    response = client.post('/food_logs', json=food_log_data, headers=headers)
    assert response.status_code == 201
    
    # Get user's logs and verify
    user = User.query.filter_by(username='testuser').first()
    response = client.get(f'/food_logs/{user.id}', headers=headers)
    assert response.status_code == 200
    logs = response.get_json()
    assert any(log['food_name'] == 'Homemade Cookies' and log['grams'] == 50 for log in logs)

def test_food_log_for_user(client, register_and_login):
    """Test fetching the food logs for a user."""
    # Create food entry and log it
    food = Food(name="Banana", calories_per_100g=89.0, protein_per_100g=1.1, carbs_per_100g=23.0, fat_per_100g=0.3)
    db.session.add(food)
    db.session.commit()

    user = User.query.filter_by(username='testuser').first()  # get user
    food_log_data = {
        'food_id': food.id,
        'grams': 200  # logging 200g of banana
    }

    # Get the JWT token from the fixture
    jwt_token = register_and_login

    # Prepare the Authorization header with the token
    headers = {
        'Authorization': f'Bearer {jwt_token}'  # Add the token to the header
    }

    # Create the food log (POST request)
    client.post('/food_logs', json=food_log_data, headers=headers)

    # Now fetch the food logs for the user
    response = client.get(f'/food_logs/{user.id}', headers=headers)  # Include the token in the header
    assert response.status_code == 200
    assert b'Banana' in response.data  # Check if food name is in the response
    assert b'200' in response.data  # Check if the grams of food logged is correct

def test_unauthorized_food_log(client):
    """Test food log creation without being logged in."""
    food = Food(name="Orange", calories_per_100g=47.0, protein_per_100g=0.9, carbs_per_100g=12.0, fat_per_100g=0.1)
    db.session.add(food)
    db.session.commit()

    # Attempt to add food log without login
    response = client.post('/food_logs', json={
        'food_id': food.id,
        'grams': 100
    })
    assert response.status_code == 401
    assert b'Missing Authorization Header' in response.data
