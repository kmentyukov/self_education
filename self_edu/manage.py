#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import (find_dotenv, load_dotenv)

filename = '.env.dev'
dotenv_file = find_dotenv(filename)

if os.path.exists(dotenv_file):
    load_dotenv(dotenv_path=dotenv_file)
else:
    exit(f'manage.py -> { filename } not found')


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'self_edu.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
