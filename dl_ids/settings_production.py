"""
Production Django settings for dl_ids project.
This file contains production-ready settings for deployment on Render.com
"""

import os
from pathlib import Path
from .settings import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-u0h4)!$@t+l%8s-@+ew3dwrcybvrrqvk+nr1y)3&kofkj2l^!q')

# Production hosts
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.render.com',  # Allow all render.com subdomains
    os.environ.get('RENDER_EXTERNAL_HOSTNAME', ''),  # Render external hostname
]

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Database configuration for production
# Use environment variables for database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files configuration for production
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Disable captcha in production for demo purposes
# You can re-enable this later if needed
CAPTCHA_ENABLED = False

# Model directories
MODELS_DIRS = os.path.join(BASE_DIR, "model")
MEAN_STD_DIRS = os.path.join(BASE_DIR, "mean_std")

# Data upload settings
DATA_UPLOAD_MAX_MEMORY_SIZE = 33554432  # 32MB

# Disable DDoS middleware in production for demo purposes
# This prevents issues with packet capture on cloud platforms
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'main.middleware.AuthMiddleware',
    # 'main.ddos_middleware.DDoSDetectionMiddleware',  # Disabled for cloud deployment
]
