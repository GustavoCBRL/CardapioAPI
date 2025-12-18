#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Collect static files
cd cardapioAPIProject
python manage.py collectstatic --no-input

# Make migrations
python manage.py makemigrations --no-input
python manage.py migrate --no-input
