#!/usr/bin/env python
"""
Script para criar superuser automaticamente
Execute: python create_superuser.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cardapioAPI.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = input('Username: ')
email = input('Email: ')
password = input('Password: ')

if User.objects.filter(username=username).exists():
    print(f'❌ Usuário {username} já existe!')
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'✅ Superuser {username} criado com sucesso!')
