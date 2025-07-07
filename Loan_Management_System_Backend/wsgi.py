"""
WSGI config for Loan_Management_System project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Loan_Management_System_Backend.settings')

application = get_wsgi_application()
application = WhiteNoise(application, root=settings.STATIC_ROOT)
