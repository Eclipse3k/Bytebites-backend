# config/development.py
from .base import BaseConfig

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = BaseConfig.get_database_url()
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    
    @classmethod
    def init_app(cls, app):
        super().init_app(app)
        print(f"Running in DEVELOPMENT mode using database: {cls.SQLALCHEMY_DATABASE_URI}")