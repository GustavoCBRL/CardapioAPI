import os
import sys
from pathlib import Path

# Add project to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / 'cardapioAPIProject'))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cardapioAPI.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Vercel serverless function handler
app = application
