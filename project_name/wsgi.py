"""
WSGI config for {{ project_name }} project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/{{ docs_version }}/howto/deployment/wsgi/
"""

import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ project_name }}.settings")

# Python 2 threading problems
if sys.version_info < (3,):
    import _strptime  # noqa

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
