"""
WSGI config for self_edu project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dotenv import find_dotenv, load_dotenv


filename = '.env.prod'
dotenv_file = find_dotenv(filename)

if os.path.exists(dotenv_file):
    load_dotenv(dotenv_path=dotenv_file)
else:
    exit(f'manage.py -> { filename } not found')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'self_edu.settings')

application = get_wsgi_application()
