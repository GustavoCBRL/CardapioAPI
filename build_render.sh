#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
cd cardapioAPIProject
python manage.py collectstatic --no-input
python manage.py migrate --no-input

# Create superuser if it doesn't exist
python manage.py shell << EOF
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get('ADMIN_USERNAME', 'admin')
email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
password = os.environ.get('ADMIN_PASSWORD', 'admin123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser {username} created successfully!')
else:
    print(f'Superuser {username} already exists')
EOF
