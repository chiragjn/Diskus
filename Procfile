web: python manage.py collectstatic --noinput;gunicorn -b 0.0.0.0:\$PORT -w 3 --env DJANGO_SETTINGS_MODULE=DiskusForums.settings DiskusForums.wsgi
