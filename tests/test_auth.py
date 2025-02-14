import pytest
from app import create_app, db
from app.models import User
from config import TestingConfig

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
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
def registered_user(client):
    """Register a user for testing login."""
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    }
    client.post('/auth/register', json=user_data)
    return user_data

@pytest.fixture
def auth_headers(client, registered_user):
    """Get authentication headers for a registered user."""
    response = client.post('/auth/login', json={
        'username': registered_user['username'],
        'password': registered_user['password']
    })
    token = response.get_json()['access_token']
    return {'Authorization': f'Bearer {token}'}

def test_register(client):
    """Test user registration."""
    # Test successful registration
    response = client.post('/auth/register', json={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert b'User created successfully' in response.data
    
    # Test duplicate username
    response = client.post('/auth/register', json={
        'username': 'newuser',
        'email': 'another@example.com',
        'password': 'password123'
    })
    assert response.status_code == 400
    assert b'Username already exists' in response.data
    
    # Test duplicate email
    response = client.post('/auth/register', json={
        'username': 'anotheruser',
        'email': 'new@example.com',
        'password': 'password123'
    })
    assert response.status_code == 400
    assert b'Email already registered' in response.data
    
    # Test missing fields
    response = client.post('/auth/register', json={
        'username': 'testuser'
    })
    assert response.status_code == 400
    assert b'Missing required fields' in response.data

def test_login(client, registered_user):
    """Test user login functionality."""
    # Test successful login with username
    response = client.post('/auth/login', json={
        'username': registered_user['username'],
        'password': registered_user['password']
    })
    assert response.status_code == 200
    assert 'access_token' in response.get_json()
    
    # Test successful login with email
    response = client.post('/auth/login', json={
        'username': registered_user['email'],
        'password': registered_user['password']
    })
    assert response.status_code == 200
    assert 'access_token' in response.get_json()
    
    # Test invalid password
    response = client.post('/auth/login', json={
        'username': registered_user['username'],
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    
    # Test non-existent user
    response = client.post('/auth/login', json={
        'username': 'nonexistent',
        'password': 'password123'
    })
    assert response.status_code == 401

def test_token_authentication(client, auth_headers):
    """Test protected routes with JWT token."""
    # Test accessing protected route with valid token
    response = client.get('/food_logs/1', headers=auth_headers)
    assert response.status_code != 401  # Should not be unauthorized
    
    # Test accessing protected route without token
    response = client.get('/food_logs/1')
    assert response.status_code == 401
    assert b'Missing Authorization Header' in response.data