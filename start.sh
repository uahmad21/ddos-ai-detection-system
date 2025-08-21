#!/bin/bash

echo "Starting DDoS AI Detection System..."

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=dl_ids.settings_production

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --settings=dl_ids.settings_production

# Start the application
echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:8000 dl_ids.wsgi:application
