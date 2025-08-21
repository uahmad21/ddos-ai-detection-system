# Use Python 3.10 slim image for Django 4.2 compatibility
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

# Make startup script executable
RUN chmod +x start.sh

# Create staticfiles directory
RUN mkdir -p staticfiles

# Expose port
EXPOSE 8000

# Start command
CMD ["./start.sh"]
