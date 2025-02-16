# config/base.py
import os
from dotenv import load_dotenv
import secrets

# Load environment variables from .env file
load_dotenv()

class BaseConfig:
    # Basic Configuration
    SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_urlsafe(32))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", secrets.token_hex(32))
    
    # AI Configuration
    AI_MODEL_NAME = os.environ.get("AI_MODEL_NAME", "default_model")
    AI_MODEL_PATH = os.environ.get("AI_MODEL_PATH", "/path/to/model")
    AI_API_KEY = os.environ.get("AI_API_KEY")
    
    # Redis configuration
    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
    
    # Rate limiting
    RATELIMIT_STORAGE_URL = REDIS_URL
    RATELIMIT_DEFAULT = "100/hour"
    RATELIMIT_STRATEGY = "fixed-window"
    
    # Cache configuration
    CACHE_TYPE = "redis"
    CACHE_REDIS_URL = REDIS_URL
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes default cache timeout

    @staticmethod
    def get_database_url():
        """Get the database URL based on environment."""
        env = os.getenv('FLASK_ENV', 'development')
        
        if env == 'testing':
            return os.getenv('DATABASE_TEST_URL', 'postgresql://jorge:4345@localhost/bytebites_test')
        elif env == 'production':
            return os.getenv('DATABASE_URL', 'postgresql://localhost/bytebites')
        else:  # development is default
            return os.getenv('DATABASE_URL', 'postgresql://localhost/bytebites_dev')

    @classmethod
    def init_app(cls, app):
        """Initialize application configuration."""
        pass