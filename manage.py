#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Automatically run pending database migrations on server boot
    if len(sys.argv) > 1 and sys.argv[1] in ('runserver', 'runserver_plus'):
        if os.environ.get('RUN_MAIN') != 'true':
            try:
                import django
                django.setup()
                from django.core.management import call_command
                print("Checking and applying pending database migrations on startup...")
                call_command('migrate', interactive=False)
                print("Database migrations applied successfully.")
            except Exception as e:
                print(f"Startup migration notice: {e}")

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
