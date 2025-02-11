# config/base.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-please-change")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-dev-key")
    AI_MODEL_NAME = os.environ.get("AI_MODEL_NAME", "default_model")
    AI_MODEL_PATH = os.environ.get("AI_MODEL_PATH", "/path/to/model")
    AI_API_KEY = os.environ.get("AI_API_KEY")