#!/bin/sh
set -e

echo "👉 Collecting static files..."
python manage.py collectstatic --noinput

echo "👉 Applying migrations..."
python manage.py migrate --noinput

echo "👉 Starting Gunicorn..."
exec gunicorn drf_starter.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --access-logfile - \
    --error-logfile -
