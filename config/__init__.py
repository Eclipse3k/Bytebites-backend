# config/__init__.py
import os

from .development import DevelopmentConfig
from .production import ProductionConfig
from .testing import TestingConfig

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Helper function to get the current config based on environment"""
    flask_config = os.environ.get('FLASK_CONFIG')
    if flask_config:
        # If specific config class is specified, use it
        return config.get(flask_config.lower(), config['default'])
    
    # Otherwise use FLASK_ENV
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env.lower(), config['default'])