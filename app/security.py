from flask import request, g
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from functools import wraps
import time
import os

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per hour", "5 per second"],
    storage_uri="memory://"  # Change to redis:// in production
)

def setup_security(app):
    # Configure CORS based on environment
    default_origins = [
        'http://localhost:8000',
        'http://127.0.0.1:8000',
        'http://localhost:5000',
        'http://127.0.0.1:5000'
    ]
    allowed_origins = os.environ.get('ALLOWED_ORIGINS', ','.join(default_origins)).split(',')
    
    # Configure CORS with more permissive settings for development
    CORS(app, resources={
        r"/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "Accept"],
            "expose_headers": ["Content-Range", "X-Total-Count"],
            "supports_credentials": True,
            "max_age": 600  # Cache preflight requests for 10 minutes
        }
    })
    
    # Configure Talisman for security headers
    csp = {
        'default-src': "'self'",
        'img-src': ["'self'", 'data:', 'https:'],
        'script-src': ["'self'", "'unsafe-inline'"],
        'style-src': ["'self'", "'unsafe-inline'"],
        'connect-src': ["'self'"] + allowed_origins
    }
    
    Talisman(
        app,
        force_https=False,  # Set to True in production
        strict_transport_security=True,
        session_cookie_secure=False,  # Set to True in production
        content_security_policy=csp
    )
    
    # Setup rate limiter
    limiter.init_app(app)
    
    @app.before_request
    def start_timer():
        g.start = time.time()
    
    @app.after_request
    def handle_response(response):
        # Add CORS headers for error responses
        origin = request.headers.get('Origin')
        if origin in allowed_origins:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Accept'
            
            # If this is a preflight request, set max age
            if request.method == 'OPTIONS':
                response.headers['Access-Control-Max-Age'] = '600'
        
        # Log request timing
        if hasattr(g, 'start'):
            total_time = time.time() - g.start
            app.logger.info(f'Request to {request.path} took {total_time:.2f}s')
            
        return response

    return app