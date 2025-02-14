from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import db
from .models import User
from datetime import datetime

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user's profile"""
    current_user_id = get_jwt_identity()
    user = db.session.get(User, int(current_user_id))
    
    return jsonify({
        "username": user.username,
        "email": user.email,
        "bio": user.bio,
        "daily_calorie_goal": user.daily_calorie_goal,
        "weight": user.weight,
        "height": user.height,
        "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else None,
        "joined_at": user.joined_at.isoformat(),
        "followers_count": user.followers_count,
        "following_count": user.following_count,
        "profile_picture_url": user.profile_picture_url
    })

@profile_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user's profile"""
    current_user_id = get_jwt_identity()
    user = db.session.get(User, int(current_user_id))
    data = request.get_json()
    
    # Update allowed fields
    if 'bio' in data:
        user.bio = data['bio']
    if 'daily_calorie_goal' in data:
        user.daily_calorie_goal = data['daily_calorie_goal']
    if 'weight' in data:
        user.weight = data['weight']
    if 'height' in data:
        user.height = data['height']
    if 'date_of_birth' in data:
        try:
            user.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"message": "Invalid date format. Use YYYY-MM-DD"}), 400
    if 'profile_picture_url' in data:
        user.profile_picture_url = data['profile_picture_url']
    
    db.session.commit()
    return jsonify({"message": "Profile updated successfully"})

@profile_bp.route('/users/<int:user_id>/follow', methods=['POST'])
@jwt_required()
def follow_user(user_id):
    """Follow a user"""
    current_user_id = get_jwt_identity()
    if int(current_user_id) == user_id:
        return jsonify({"message": "Cannot follow yourself"}), 400
        
    current_user = db.session.get(User, int(current_user_id))
    user_to_follow = db.session.get(User, user_id)
    
    if not user_to_follow:
        return jsonify({"message": "User not found"}), 404
        
    current_user.follow(user_to_follow)
    db.session.commit()
    return jsonify({"message": f"Now following {user_to_follow.username}"})

@profile_bp.route('/users/<int:user_id>/unfollow', methods=['POST'])
@jwt_required()
def unfollow_user(user_id):
    """Unfollow a user"""
    current_user_id = get_jwt_identity()
    current_user = db.session.get(User, int(current_user_id))
    user_to_unfollow = db.session.get(User, user_id)
    
    if not user_to_unfollow:
        return jsonify({"message": "User not found"}), 404
        
    current_user.unfollow(user_to_unfollow)
    db.session.commit()
    return jsonify({"message": f"Unfollowed {user_to_unfollow.username}"})

@profile_bp.route('/feed', methods=['GET'])
@jwt_required()
def get_feed():
    """Get food logs from followed users"""
    current_user_id = get_jwt_identity()
    user = db.session.get(User, int(current_user_id))
    
    feed_logs = user.get_feed().limit(50).all()  # Limit to last 50 entries
    
    return jsonify([{
        "username": log.user.username,
        "food_name": log.food.name,
        "grams": log.grams,
        "calories": (log.food.calories_per_100g * log.grams) / 100,
        "log_date": log.log_date.isoformat()
    } for log in feed_logs])

@profile_bp.route('/users/<int:user_id>/profile', methods=['GET'])
@jwt_required()
def get_user_profile(user_id):
    """Get another user's public profile"""
    current_user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
        
    current_user = db.session.get(User, int(current_user_id))
    is_following = current_user.is_following(user) if current_user else False
    
    return jsonify({
        "username": user.username,
        "bio": user.bio,
        "profile_picture_url": user.profile_picture_url,
        "followers_count": user.followers_count,
        "following_count": user.following_count,
        "is_following": is_following,
        "joined_at": user.joined_at.isoformat()
    })