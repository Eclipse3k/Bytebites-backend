from flask import request, g
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps
import time
import os

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per hour", "5 per second"],
    storage_uri="memory://"  # Change to redis:// in production
)

def setup_security(app):
    # More permissive CORS for development
    allowed_origins = os.environ.get('ALLOWED_ORIGINS', '*')
    
    CORS(app, resources={
        r"/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Setup rate limiter with more permissive limits for development
    limiter.init_app(app)
    
    # Simplified security headers for development
    @app.after_request
    def add_security_headers(response):
        if app.debug:
            response.headers['Access-Control-Allow-Origin'] = '*'
        else:
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        return response
    
    # Request timing middleware
    @app.before_request
    def start_timer():
        g.start = time.time()
    
    @app.after_request
    def log_request(response):
        if hasattr(g, 'start'):
            total_time = time.time() - g.start
            app.logger.info(f'Request to {request.path} took {total_time:.2f}s')
        return response
    
    return app