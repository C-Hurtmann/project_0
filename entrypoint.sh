#!/bin/bash

echo "Running Django migrations..."
python manage.py makemigrations
python manage.py migrate

exec "$@"