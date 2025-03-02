# filepath: /home/jorge/projects/bytebites-backend/app/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from . import db
from .models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Basic validation
    if not username or not email or not password:
        return jsonify({"message": "Missing required fields"}), 400

    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered"}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201
    
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    login_value = data.get('username')
    password = data.get('password')

    if not login_value or not password:
        return jsonify({"message": "Missing login or password"}), 400

    if "@" in login_value:
        user = User.query.filter_by(email=login_value).first()
    else:
        user = User.query.filter_by(username=login_value).first()

    if user and user.check_password(password):
        # Convert user ID to string when creating the token
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            "message": "Logged in successfully",
            "access_token": access_token
        }), 200
    else:
        return jsonify({"message": "Invalid login or password"}), 401