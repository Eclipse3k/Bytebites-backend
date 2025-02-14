# config/development.py
from .base import BaseConfig
import os

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://localhost/bytebites_dev")
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour