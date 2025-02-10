from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

class Config:
    # Secret key for session management and other security needs
    SECRET_KEY = os.environ.get("SECRET_KEY")
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # AI-related configuration settings
    AI_MODEL_NAME = os.environ.get("AI_MODEL_NAME") or "default_model"
    AI_MODEL_PATH = os.environ.get("AI_MODEL_PATH") or "/path/to/your/model"
    AI_API_KEY = os.environ.get("AI_API_KEY") or "your_api_key_here"
