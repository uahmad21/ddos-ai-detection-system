# Use Python 3.10 slim image for Django 5.1.4 compatibility
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=dl_ids.settings_production

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements_minimal.txt .
RUN pip install --no-cache-dir -r requirements_minimal.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput --settings=dl_ids.settings_production

# Run database migrations
RUN python manage.py migrate --settings=dl_ids.settings_production

# Expose port
EXPOSE 8000

# Start command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "dl_ids.wsgi:application"]
