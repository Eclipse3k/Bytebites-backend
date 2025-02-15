from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from . import db
from .models import Food, FoodLog

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/foods', methods=['GET'])
def search_foods():
    query = request.args.get('query', '')
    
    # Using unaccent and case-insensitive search
    foods = Food.query.filter(
        func.unaccent(func.lower(Food.name)).like(
            func.unaccent(func.lower(f"%{query}%"))
        )
    ).all()
    
    return jsonify([{
        "id": food.id,
        "name": food.name,
        "calories_per_100g": food.calories_per_100g,
        "protein_per_100g": food.protein_per_100g,
        "carbs_per_100g": food.carbs_per_100g,
        "fat_per_100g": food.fat_per_100g
    } for food in foods])

@routes_bp.route('/foods', methods=['POST'])
@jwt_required()
def create_food():
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('calories_per_100g'):
        return jsonify({"message": "Name and calories per 100g are required"}), 400
        
    if Food.query.filter_by(name=data['name']).first():
        return jsonify({"message": "A food with this name already exists"}), 400
    
    # Validate calories
    calories = float(data['calories_per_100g'])
    if calories <= 0:
        return jsonify({"message": "Calories per 100g must be positive"}), 400
    if calories > 1000:
        return jsonify({"message": "Calories per 100g seems unreasonably high"}), 400
        
    food = Food(
        name=data['name'],
        calories_per_100g=calories,
        protein_per_100g=data.get('protein_per_100g'),
        carbs_per_100g=data.get('carbs_per_100g'),
        fat_per_100g=data.get('fat_per_100g')
    )
    
    db.session.add(food)
    db.session.commit()
    
    return jsonify({
        "message": "Food created successfully",
        "food": {
            "id": food.id,
            "name": food.name,
            "calories_per_100g": food.calories_per_100g,
            "protein_per_100g": food.protein_per_100g,
            "carbs_per_100g": food.carbs_per_100g,
            "fat_per_100g": food.fat_per_100g
        }
    }), 201

@routes_bp.route('/food_logs', methods=['POST'])
@jwt_required()
def log_food():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    if not data or 'food_id' not in data or 'grams' not in data:
        return jsonify({"message": "Missing required fields"}), 422

    # Validate grams
    grams = float(data['grams'])
    if grams <= 0:
        return jsonify({"message": "Grams must be greater than 0"}), 422
    if grams > 5000:  # 5kg limit
        return jsonify({"message": "Grams amount seems unusually large"}), 422

    food = db.session.get(Food, data['food_id'])
    if not food:
        return jsonify({"message": "Food not found"}), 404

    food_log = FoodLog(
        user_id=int(current_user_id),
        food_id=data['food_id'],
        grams=grams
    )
    
    db.session.add(food_log)
    db.session.commit()
    
    return jsonify({"message": "Food log created successfully"}), 201

@routes_bp.route('/food_logs/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_food_logs(user_id):
    current_user_id = get_jwt_identity()
    if int(current_user_id) != user_id:
        return jsonify({"message": "Unauthorized"}), 403
        
    logs = FoodLog.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "food_name": log.food.name,
        "grams": log.grams,
        "calories": (log.food.calories_per_100g * log.grams) / 100,
        "log_date": log.log_date
    } for log in logs]), 200