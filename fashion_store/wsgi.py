"""
WSGI config for fashion_store project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fashion_store.settings')

application = get_wsgi_application()
