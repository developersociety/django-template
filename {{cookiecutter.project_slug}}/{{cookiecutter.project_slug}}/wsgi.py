"""
WSGI config for {{ cookiecutter.project_slug }} project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
