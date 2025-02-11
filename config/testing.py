# config/testing.py
from .base import BaseConfig
import os

class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL", "postgresql://localhost/bytebites_test")
    JWT_ACCESS_TOKEN_EXPIRES = 300  # 5 minutes