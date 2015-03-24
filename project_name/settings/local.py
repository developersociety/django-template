# -*- coding: utf-8 -*-

from .base import *  # NOQA @UnusedWildImport


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{{ project_name }}',
        'USER': '',
        'PASSWORD': os.environ.get('DJANGO_DATABASE_PASSWORD', ''),
        'PORT': '5432',
    },
}

DEBUG = True


TEMPALTE_DEBUG = DEBUG


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

