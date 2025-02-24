#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers for all responses
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, Accept')
        self.send_header('Access-Control-Max-Age', '600')
        return super().end_headers()

    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(204)
        self.end_headers()

def run_test_server():
    # Change to the project root directory first, then to test-client
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    test_client_dir = os.path.join(project_root, 'test-client')
    
    if not os.path.exists(test_client_dir):
        raise FileNotFoundError(f"Test client directory not found at: {test_client_dir}")
    
    os.chdir(test_client_dir)
    
    port = 8000
    # Using empty string as host allows connections from both localhost and 127.0.0.1
    host = ''
    print(f"Starting test client server at:")
    print(f"http://localhost:{port}")
    print(f"http://127.0.0.1:{port}")
    print("Use Ctrl+C to stop the server")
    
    httpd = HTTPServer((host, port), CORSRequestHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    run_test_server()