from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import get_config
from apscheduler.schedulers.background import BackgroundScheduler

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=None):
    """Factory function to create a Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    if config_class is None:
        config_class = get_config()
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Setup security features
    from .security import setup_security
    app = setup_security(app)
    
    # Custom JWT error handler
    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        return jsonify({"message": "Invalid token"}), 422
    
    # Register blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from .routes import routes_bp
    app.register_blueprint(routes_bp)
    
    from .profile import profile_bp
    app.register_blueprint(profile_bp, url_prefix='/api')
    
    # Set up background job to clean up old logs every 1 week
    from .utils import cleanup_old_logs
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=cleanup_old_logs, trigger="interval", weeks=1)
    scheduler.start()
    
    return app
