"""Test cases for food management functionality."""
import pytest
from app.models import Food
from app.feature_flags import Feature, FeatureFlags

def test_create_food(client, auth_headers):
    """Test creating a custom food item."""
    food_data = {
        'name': 'Custom Pizza',
        'calories_per_100g': 267.0,
        'protein_per_100g': 11.0,
        'carbs_per_100g': 33.0,
        'fat_per_100g': 9.8
    }
    
    response = client.post('/foods', json=food_data, headers=auth_headers)
    assert response.status_code == 201
    assert 'Food created successfully' in response.get_json()['message']
    
    # Verify food was created with correct data
    food = response.get_json()['food']
    assert food['name'] == food_data['name']
    assert food['calories_per_100g'] == food_data['calories_per_100g']

def test_create_food_validation(client, auth_headers):
    """Test food creation validation."""
    # Test duplicate food name
    food_data = {
        'name': 'Test Apple',  # Same name as sample_food fixture
        'calories_per_100g': 150.0
    }
    response = client.post('/foods', json=food_data, headers=auth_headers)
    assert response.status_code == 400
    assert 'already exists' in response.get_json()['message']
    
    # Test missing required fields
    incomplete_data = {'name': 'Incomplete Food'}
    response = client.post('/foods', json=incomplete_data, headers=auth_headers)
    assert response.status_code == 400
    assert 'required' in response.get_json()['message']

def test_search_foods(client, sample_food):
    """Test food search functionality."""
    # Test exact match
    response = client.get('/foods?query=Test Apple')
    assert response.status_code == 200
    foods = response.get_json()
    assert len(foods) == 1
    assert foods[0]['name'] == 'Test Apple'
    
    # Test partial match
    response = client.get('/foods?query=Apple')
    assert response.status_code == 200
    foods = response.get_json()
    assert len(foods) > 0
    assert any(food['name'] == 'Test Apple' for food in foods)
    
    # Test case insensitive search
    response = client.get('/foods?query=apple')
    assert response.status_code == 200
    foods = response.get_json()
    assert len(foods) > 0
    assert any(food['name'] == 'Test Apple' for food in foods)

def test_nutrition_tracking_feature_flag(client, auth_headers):
    """Test nutrition tracking feature flag."""
    food_data = {
        'name': 'Feature Test Food',
        'calories_per_100g': 200.0,
        'protein_per_100g': 10.0,
        'carbs_per_100g': 25.0,
        'fat_per_100g': 8.0
    }
    
    # Test with feature enabled
    FeatureFlags.enable(Feature.NUTRITION_TRACKING)
    response = client.post('/foods', json=food_data, headers=auth_headers)
    assert response.status_code == 201
    food = response.get_json()['food']
    assert 'protein_per_100g' in food
    assert 'carbs_per_100g' in food
    assert 'fat_per_100g' in food
    
    # Test with feature disabled
    FeatureFlags.disable(Feature.NUTRITION_TRACKING)
    response = client.get('/foods?query=Feature Test Food')
    foods = response.get_json()
    assert foods[0]['protein'] is None
    assert foods[0]['carbs'] is None
    assert foods[0]['fat'] is None