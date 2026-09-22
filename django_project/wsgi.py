"""
WSGI config for django_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import logging
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

application = get_wsgi_application()

# Run database migrations on WSGI startup (Render/production container boot)
try:
    from django.core.management import call_command
    call_command('migrate', interactive=False)
except Exception as exc:
    logging.getLogger(__name__).warning(f"Startup database migration in wsgi notice: {exc}")
