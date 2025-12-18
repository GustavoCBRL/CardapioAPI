#!/bin/bash

# Collect static files
python cardapioAPIProject/manage.py collectstatic --no-input

# Make migrations
python cardapioAPIProject/manage.py makemigrations --no-input
python cardapioAPIProject/manage.py migrate --no-input
