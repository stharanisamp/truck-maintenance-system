import sys
import os

# Ensure the project root directory is in sys.path for absolute imports
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Import the initialized Flask application instance
from app import app

# Vercel Serverless Function entry point
# Flask app is exposed as 'app'
