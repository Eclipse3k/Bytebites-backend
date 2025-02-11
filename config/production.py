# config/production.py
from .base import BaseConfig
import os

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours