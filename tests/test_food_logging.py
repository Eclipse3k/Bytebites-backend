"""Test cases for food logging functionality."""
import pytest
from app.models import FoodLog, Food
from datetime import datetime
from app import db

def test_create_food_log(client, auth_headers, sample_food, app):
    """Test creating a food log entry."""
    with app.app_context():
        sample_food = db.session.query(Food).filter_by(name="Test Apple").first()
        food_log_data = {
            'food_id': sample_food.id,
            'grams': 150
        }
        response = client.post('/food_logs', json=food_log_data, headers=auth_headers)
        assert response.status_code == 201
        assert 'Food log created successfully' in response.get_json()['message']

def test_food_log_validation(client, auth_headers, app):
    """Test food log validation."""
    with app.app_context():
        # Test non-existent food
        invalid_log_data = {
            'food_id': 99999,  # Non-existent food ID
            'grams': 100
        }
        response = client.post('/food_logs', json=invalid_log_data, headers=auth_headers)
        assert response.status_code == 404
        assert 'Food not found' in response.get_json()['message']

        # Test missing required fields
        incomplete_data = {'food_id': 1}  # Missing grams
        response = client.post('/food_logs', json=incomplete_data, headers=auth_headers)
        assert response.status_code == 422
        assert 'Missing required fields' in response.get_json()['message']

def test_get_user_food_logs(client, auth_headers, registered_user, sample_food, app):
    """Test retrieving user's food logs."""
    with app.app_context():
        sample_food = db.session.query(Food).filter_by(name="Test Apple").first()
        # Create a food log first
        food_log_data = {
            'food_id': sample_food.id,
            'grams': 200
        }
        client.post('/food_logs', json=food_log_data, headers=auth_headers)

        # Get user's logs
        response = client.get(f'/food_logs/1', headers=auth_headers)
        assert response.status_code == 200
        logs = response.get_json()
        assert len(logs) > 0
        assert logs[0]['food_name'] == sample_food.name
        assert logs[0]['grams'] == 200
        assert 'log_date' in logs[0]
        assert 'calories' in logs[0]

def test_unauthorized_access(client, auth_headers, app):
    """Test unauthorized access to food logs."""
    with app.app_context():
        # Try to access another user's logs
        response = client.get('/food_logs/999', headers=auth_headers)
        assert response.status_code == 403
        assert 'Unauthorized' in response.get_json()['message']

        # Try to create log without authentication
        food_log_data = {
            'food_id': 1,
            'grams': 100
        }
        response = client.post('/food_logs', json=food_log_data)
        assert response.status_code == 401
        assert b'Missing Authorization Header' in response.data

def test_food_log_calculations(client, auth_headers, app, sample_food):
    """Test food log calorie calculations."""
    with app.app_context():
        sample_food = db.session.query(Food).filter_by(name="Test Apple").first()
        # Create a food log with known values
        food_log_data = {
            'food_id': sample_food.id,
            'grams': 150  # 150g of a food with 52 calories per 100g
        }
        client.post('/food_logs', json=food_log_data, headers=auth_headers)

        # Verify calculations in retrieved logs
        response = client.get('/food_logs/1', headers=auth_headers)
        logs = response.get_json()
        log = logs[0]
        
        # Calculate expected calories: (52 cal/100g * 150g) / 100 = 78 calories
        expected_calories = (sample_food.calories_per_100g * food_log_data['grams']) / 100
        assert log['calories'] == expected_calories

def test_zero_grams_food_log(client, auth_headers, sample_food, app):
    """Test creating a food log with zero grams."""
    with app.app_context():
        sample_food = db.session.query(Food).filter_by(name="Test Apple").first()
        food_log_data = {
            'food_id': sample_food.id,
            'grams': 0
        }
        response = client.post('/food_logs', json=food_log_data, headers=auth_headers)
        assert response.status_code == 422
        assert 'Grams must be greater than 0' in response.get_json()['message']

def test_negative_grams_food_log(client, auth_headers, sample_food, app):
    """Test creating a food log with negative grams."""
    with app.app_context():
        sample_food = db.session.query(Food).filter_by(name="Test Apple").first()
        food_log_data = {
            'food_id': sample_food.id,
            'grams': -50
        }
        response = client.post('/food_logs', json=food_log_data, headers=auth_headers)
        assert response.status_code == 422
        assert 'Grams must be greater than 0' in response.get_json()['message']

def test_large_grams_food_log(client, auth_headers, sample_food, app):
    """Test creating a food log with unusually large grams."""
    with app.app_context():
        sample_food = db.session.query(Food).filter_by(name="Test Apple").first()
        food_log_data = {
            'food_id': sample_food.id,
            'grams': 10000  # 10kg of food
        }
        response = client.post('/food_logs', json=food_log_data, headers=auth_headers)
        assert response.status_code == 422
        assert 'Grams amount seems unusually large' in response.get_json()['message']

def test_float_precision_food_log(client, auth_headers, sample_food, app):
    """Test handling of floating point precision in food logs."""
    with app.app_context():
        sample_food = db.session.query(Food).filter_by(name="Test Apple").first()
        food_log_data = {
            'food_id': sample_food.id,
            'grams': 33.333333
        }
        response = client.post('/food_logs', json=food_log_data, headers=auth_headers)
        assert response.status_code == 201
        
        # Check the logs to verify precision was maintained
        response = client.get('/food_logs/1', headers=auth_headers)
        logs = response.get_json()
        assert abs(logs[0]['grams'] - 33.333333) < 0.0001  # Check precision was maintained
        
        # Verify calorie calculation precision
        expected_calories = (sample_food.calories_per_100g * 33.333333) / 100
        assert abs(logs[0]['calories'] - expected_calories) < 0.0001

def test_multiple_logs_same_food(client, auth_headers, sample_food, app):
    """Test creating multiple logs for the same food item."""
    with app.app_context():
        sample_food = db.session.query(Food).filter_by(name="Test Apple").first()
        # Create three logs for the same food
        for grams in [100, 150, 200]:
            response = client.post('/food_logs', json={
                'food_id': sample_food.id,
                'grams': grams
            }, headers=auth_headers)
            assert response.status_code == 201
        
        # Verify all logs were created
        response = client.get('/food_logs/1', headers=auth_headers)
        logs = response.get_json()
        assert len(logs) == 3
        assert sorted([log['grams'] for log in logs]) == [100, 150, 200]