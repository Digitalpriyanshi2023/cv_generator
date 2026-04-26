import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_app import app

# Vercel needs the app to be named 'app'
# Since we already named it 'app' in web_app.py, this works.
