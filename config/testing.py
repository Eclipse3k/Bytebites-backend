# config/testing.py
from .base import BaseConfig
import os
import secrets

class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL", "postgresql://jorge:4345@localhost/bytebites_test")
    JWT_SECRET_KEY = os.environ.get("TEST_JWT_SECRET_KEY", secrets.token_hex(32))
    JWT_ACCESS_TOKEN_EXPIRES = 300  # 5 minutes