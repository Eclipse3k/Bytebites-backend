"""Common test fixtures and utilities."""
import pytest
from app import create_app, db
from app.models import User, Food
from config import TestingConfig

@pytest.fixture
def app():
    """Fixture to create the test app and database tables."""
    app = create_app(TestingConfig)
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def registered_user(client):
    """Create and return a registered user."""
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    }
    client.post('/auth/register', json=user_data)
    return user_data

@pytest.fixture
def auth_token(client, registered_user):
    """Get an authentication token for the registered user."""
    response = client.post('/auth/login', json={
        'username': registered_user['username'],
        'password': registered_user['password']
    })
    return response.get_json()['access_token']

@pytest.fixture
def auth_headers(auth_token):
    """Get headers with authentication token."""
    return {'Authorization': f'Bearer {auth_token}'}

@pytest.fixture
def sample_food(app):
    """Create and return a sample food item."""
    with app.app_context():
        # Check if the food already exists
        food = db.session.query(Food).filter_by(name="Test Apple").first()
        if not food:
            food = Food(
                name="Test Apple",
                calories_per_100g=52.0,
                protein_per_100g=0.3,
                carbs_per_100g=14.0,
                fat_per_100g=0.2
            )
            db.session.add(food)
            db.session.commit()
        return food