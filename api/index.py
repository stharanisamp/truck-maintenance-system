import sys
import os

# Ensure the project root directory is in sys.path for absolute imports
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Import the initialized Flask application instance
from app import app

# Vercel WSGI PATH_INFO fix middleware: restores user-requested URL from x-matched-path
class VercelPathFix:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        matched_path = (
            environ.get('HTTP_X_MATCHED_PATH')
            or environ.get('HTTP_X_FORWARDED_URI')
            or environ.get('HTTP_X_INVOKE_PATH')
        )
        if matched_path:
            clean_path = matched_path.split('?')[0]
            if clean_path and clean_path != '/api/index':
                environ['PATH_INFO'] = clean_path
            elif clean_path == '/api/index':
                environ['PATH_INFO'] = '/'
        elif environ.get('PATH_INFO') == '/api/index':
            environ['PATH_INFO'] = '/'
        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPathFix(app.wsgi_app)
