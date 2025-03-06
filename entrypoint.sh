#!/bin/bash

echo "Running Django migrations..."
python manage.py makemigrations
python manage.py migrate

# echo "Collecting static files..."
# python manage.py collectstatic --noinput

exec "$@"