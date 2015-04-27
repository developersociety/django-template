# -*- coding: utf-8 -*-

from .base import *  # NOQA @UnusedWildImport


DEBUG = True

TEMPLATE_DEBUG = DEBUG


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{{ project_name }}_django',
        'USER': '',
        'PASSWORD': '',
        'PORT': '',
    },
}

INTERNAL_IPS = (
    '127.0.0.1',
)

INSTALLED_APPS.append(
    'debug_toolbar',
)

MIDDLEWARE_CLASSES.append(
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

COVERAGE_EXCLUDES_FOLDERS = ['/var/envs/{{ project_name }}/lib/python2']

SECRET_KEY = "{{ project_name }}"
