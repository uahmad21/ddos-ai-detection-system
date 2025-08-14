"""
WSGI config for dl_ids project in production.
"""

import os

from django.core.wsgi import get_wsgi_application

# Set production settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dl_ids.settings_production')

application = get_wsgi_application()
