# -*- coding: utf-8 -*-

import os

from .base import *  # NOQA @UnusedWildImport


DEBUG = True

TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DJANGO_DATABASE_NAME', '{{ project_name }}_django'),
        'USER': '',
        'PASSWORD': '',
        'PORT': '',
    },
}

INTERNAL_IPS = (
    '127.0.0.1',
)

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE_CLASSES = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE_CLASSES

COVERAGE_EXCLUDES_FOLDERS = ['/var/envs/{{ project_name }}/lib/python2']

SECRET_KEY = '{{ project_name }}'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
