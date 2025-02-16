# config/production.py
from .base import BaseConfig
import os

class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = BaseConfig.get_database_url()
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours
    
    @classmethod
    def init_app(cls, app):
        super().init_app(app)
        # Add warning for production mode
        if not os.environ.get('DATABASE_URL'):
            raise ValueError(
                "Production mode requires DATABASE_URL to be set in environment variables"
            )