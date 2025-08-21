"""
Production Django settings for dl_ids project.
This file contains production-ready settings for deployment on Render.com
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-u0h4)!$@t+l%8s-@+ew3dwrcybvrrqvk+nr1y)3&kofkj2l^!q')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Production hosts
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.render.com',  # Allow all render.com subdomains
    '.fly.dev',     # Allow all fly.dev subdomains
    'df-defence.fly.dev',  # Specific Fly.io hostname
    '172.19.0.0/16',  # Allow Fly.io internal IP range
    '172.20.0.0/16',  # Allow Fly.io internal IP range
    '172.21.0.0/16',  # Allow Fly.io internal IP range
    '172.22.0.0/16',  # Allow Fly.io internal IP range
    '172.23.0.0/16',  # Allow Fly.io internal IP range
    '172.24.0.0/16',  # Allow Fly.io internal IP range
    '172.25.0.0/16',  # Allow Fly.io internal IP range
    '172.26.0.0/16',  # Allow Fly.io internal IP range
    '172.27.0.0/16',  # Allow Fly.io internal IP range
    '172.28.0.0/16',  # Allow Fly.io internal IP range
    '172.29.0.0/16',  # Allow Fly.io internal IP range
    '172.30.0.0/16',  # Allow Fly.io internal IP range
    '172.31.0.0/16',  # Allow Fly.io internal IP range
    os.environ.get('RENDER_EXTERNAL_HOSTNAME', ''),  # Render external hostname
    os.environ.get('FLY_APP_NAME', '') + '.fly.dev',  # Fly.io hostname
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main.apps.MainConfig',
    # 'captcha',  # Removed for production deployment
]

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

ROOT_URLCONF = 'dl_ids.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dl_ids.wsgi.application'

# Database configuration for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = False

# Static files configuration for production
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Model directories
MODELS_DIRS = os.path.join(BASE_DIR, "model")
MEAN_STD_DIRS = os.path.join(BASE_DIR, "mean_std")

# Data upload settings
DATA_UPLOAD_MAX_MEMORY_SIZE = 33554432  # 32MB

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

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
