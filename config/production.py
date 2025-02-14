# config/production.py
from .base import BaseConfig
import os

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://localhost/bytebites")
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours