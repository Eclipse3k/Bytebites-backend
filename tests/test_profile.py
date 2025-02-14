"""Test cases for user profiles and social features."""
import pytest
from datetime import date
from app.models import User, FoodLog, Food
from app import db  # Add missing import

@pytest.fixture
def second_user(client):
    """Create a second user for testing social features."""
    user_data = {
        'username': 'testuser2',
        'email': 'test2@example.com',
        'password': 'password123'
    }
    client.post('/auth/register', json=user_data)
    return user_data

@pytest.fixture
def second_user_token(client, second_user):
    """Get auth token for second user."""
    response = client.post('/auth/login', json={
        'username': second_user['username'],
        'password': second_user['password']
    })
    return response.get_json()['access_token']

def test_update_profile(client, auth_headers):
    """Test updating user profile information."""
    profile_data = {
        'bio': 'I love healthy food!',
        'daily_calorie_goal': 2000,
        'weight': 70.5,
        'height': 175.0,
        'date_of_birth': '1990-01-01',
        'profile_picture_url': 'https://example.com/photo.jpg'
    }
    
    # Update profile
    response = client.put('/api/profile', json=profile_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Profile updated successfully'
    
    # Verify updated profile
    response = client.get('/api/profile', headers=auth_headers)
    profile = response.get_json()
    assert profile['bio'] == profile_data['bio']
    assert profile['daily_calorie_goal'] == profile_data['daily_calorie_goal']
    assert profile['weight'] == profile_data['weight']
    assert profile['height'] == profile_data['height']
    assert profile['date_of_birth'] == profile_data['date_of_birth']
    assert profile['profile_picture_url'] == profile_data['profile_picture_url']

def test_follow_unfollow_user(client, auth_headers, second_user, second_user_token):
    """Test following and unfollowing users."""
    # Get second user's ID
    response = client.get('/api/profile', headers={'Authorization': f'Bearer {second_user_token}'})
    second_user_profile = response.get_json()
    
    # First user follows second user
    response = client.post(f'/api/users/2/follow', headers=auth_headers)
    assert response.status_code == 200
    assert f"Now following {second_user['username']}" in response.get_json()['message']
    
    # Verify follower counts
    response = client.get('/api/profile', headers=auth_headers)
    profile = response.get_json()
    assert profile['following_count'] == 1
    assert profile['followers_count'] == 0
    
    # Second user's profile should show one follower
    response = client.get('/api/users/2/profile', headers=auth_headers)
    profile = response.get_json()
    assert profile['followers_count'] == 1
    assert profile['following_count'] == 0
    assert profile['is_following'] == True
    
    # Unfollow second user
    response = client.post(f'/api/users/2/unfollow', headers=auth_headers)
    assert response.status_code == 200
    assert f"Unfollowed {second_user['username']}" in response.get_json()['message']
    
    # Verify counts after unfollowing
    response = client.get('/api/profile', headers=auth_headers)
    profile = response.get_json()
    assert profile['following_count'] == 0

def test_feed(client, auth_headers, second_user_token, app):
    """Test user feed with followed users."""
    with app.app_context():
        # Create some food entries
        food1 = Food(name="Apple", calories_per_100g=52.0)
        food2 = Food(name="Banana", calories_per_100g=89.0)
        db.session.add_all([food1, food2])
        db.session.commit()
        
        # Second user logs some food
        headers2 = {'Authorization': f'Bearer {second_user_token}'}
        client.post('/food_logs', json={'food_id': food1.id, 'grams': 100}, headers=headers2)
        
        # First user follows second user
        client.post('/api/users/2/follow', headers=auth_headers)
        
        # First user logs some food
        client.post('/food_logs', json={'food_id': food2.id, 'grams': 150}, headers=auth_headers)
        
        # Check feed
        response = client.get('/api/feed', headers=auth_headers)
        assert response.status_code == 200
        
        feed = response.get_json()
        assert len(feed) == 2  # Should see both users' logs
        assert any(log['food_name'] == 'Apple' and log['username'] == 'testuser2' for log in feed)
        assert any(log['food_name'] == 'Banana' and log['username'] == 'testuser' for log in feed)

def test_view_other_profile(client, auth_headers, second_user):
    """Test viewing another user's profile."""
    response = client.get('/api/users/2/profile', headers=auth_headers)
    assert response.status_code == 200
    
    profile = response.get_json()
    assert profile['username'] == second_user['username']
    assert 'email' not in profile  # Email should not be exposed
    assert 'followers_count' in profile
    assert 'following_count' in profile
    assert 'is_following' in profile
    assert 'joined_at' in profile

def test_invalid_follow_operations(client, auth_headers):
    """Test invalid follow operations."""
    # Try to follow non-existent user
    response = client.post('/api/users/999/follow', headers=auth_headers)
    assert response.status_code == 404
    assert 'User not found' in response.get_json()['message']
    
    # Try to follow self
    response = client.post('/api/users/1/follow', headers=auth_headers)
    assert response.status_code == 400
    assert 'Cannot follow yourself' in response.get_json()['message']