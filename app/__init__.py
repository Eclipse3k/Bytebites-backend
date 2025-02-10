from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('app.config.Config')    
    
	# Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Register blueprints (we'll do that later for routes)
    from .auth import auth_bp
    #from .routes import routes_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    #app.register_blueprint(routes_bp, url_prefix='/api')
    
    return app
