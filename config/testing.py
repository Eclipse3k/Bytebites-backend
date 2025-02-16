# config/testing.py
from .base import BaseConfig
import os
import secrets

class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = BaseConfig.get_database_url()
    JWT_SECRET_KEY = os.environ.get("TEST_JWT_SECRET_KEY", secrets.token_hex(32))
    JWT_ACCESS_TOKEN_EXPIRES = 300  # 5 minutes
    
    @classmethod
    def init_app(cls, app):
        super().init_app(app)
        # Add warning for test database
        print("WARNING: Running in TESTING mode using test database:", cls.SQLALCHEMY_DATABASE_URI)