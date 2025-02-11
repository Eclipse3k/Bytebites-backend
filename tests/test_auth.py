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

def test_register(client):
    """Test user registration."""
    # Test successful registration
    response = client.post('/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert b'User created successfully' in response.data
    
    # Test duplicate username
    response = client.post('/auth/register', json={
        'username': 'testuser',
        'email': 'another@example.com',
        'password': 'password123'
    })
    assert response.status_code == 400
    assert b'Username already exists' in response.data
    
    # Test duplicate email
    response = client.post('/auth/register', json={
        'username': 'anotheruser',
        'email': 'test@example.com',
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

def test_login(client):
    """Test user login."""
    # First register a user
    client.post('/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    # Test successful login with username
    response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert b'Logged in successfully' in response.data
    
    # Test successful login with email
    response = client.post('/auth/login', json={
        'username': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert b'Logged in successfully' in response.data
    
    # Test invalid password
    response = client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert b'Invalid login or password' in response.data
    
    # Test non-existent user
    response = client.post('/auth/login', json={
        'username': 'nonexistent',
        'password': 'password123'
    })
    assert response.status_code == 401
    assert b'Invalid login or password' in response.data
    
    # Test missing fields
    response = client.post('/auth/login', json={
        'username': 'testuser'
    })
    assert response.status_code == 400
    assert b'Missing login or password' in response.data