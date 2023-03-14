#!/bin/bash

python manage.py migrate --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

gunicorn project.network.wsgi:application --bind 0.0.0.0:8000 --workers 8 --reload --preload