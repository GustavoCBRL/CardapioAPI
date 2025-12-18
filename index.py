import os
import sys
from pathlib import Path

# Add project to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / 'cardapioAPIProject'))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cardapioAPI.settings')

# Import Django
import django
django.setup()

# Run migrations on Vercel
if os.environ.get('VERCEL'):
    from django.core.management import call_command
    from django.contrib.auth import get_user_model
    
    try:
        call_command('migrate', '--no-input')
        
        # Create superuser automatically if it doesn't exist
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password=admin_password
            )
            print("Superuser 'admin' created successfully")
    except Exception as e:
        print(f"Setup error: {e}")

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Vercel serverless function handler
app = application
