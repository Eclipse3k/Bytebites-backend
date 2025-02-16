# config/__init__.py
import os
import sys

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
    # First check if we're running tests
    if 'pytest' in sys.modules:
        return TestingConfig
    
    # Then check for explicit config setting
    flask_config = os.environ.get('FLASK_CONFIG')
    if flask_config:
        config_class = config.get(flask_config.lower())
        if not config_class:
            raise ValueError(f"Invalid FLASK_CONFIG value: {flask_config}")
        return config_class
    
    # Finally check FLASK_ENV
    env = os.environ.get('FLASK_ENV', 'development').lower()
    if env not in config:
        print(f"Warning: Unknown environment '{env}', using development config")
        return config['default']
    
    return config[env]