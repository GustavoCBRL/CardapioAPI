web: cd cardapioAPIProject && python manage.py collectstatic --noinput && python manage.py migrate && gunicorn --bind 0.0.0.0:$PORT cardapioAPI.wsgi:application
