# config/__init__.py
import os

# Import all config classes
from .development import DevelopmentConfig
from .production import ProductionConfig
from .testing import TestingConfig

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Helper function to get the current config based on environment"""
    env = os.environ.get('FLASK_ENV', 'default')
    return config.get(env, config['default'])