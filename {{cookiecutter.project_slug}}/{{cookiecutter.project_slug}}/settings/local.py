from importlib import import_module
import os

from .base import *  # NOQA @UnusedWildImport


DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DJANGO_DATABASE_NAME', '{{ cookiecutter.project_slug }}_django'),
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
    'django_extensions',
]


# Add flat theme if module is installed.
try:
    import_module('flat')
except ImportError:
    pass
else:
    INSTALLED_APPS.insert(0, 'flat')


MIDDLEWARE_CLASSES = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE_CLASSES


COVERAGE_EXCLUDES_FOLDERS = ['/var/envs/{{ cookiecutter.project_slug }}/lib/python2']


SECRET_KEY = '{{ cookiecutter.project_slug }}'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Only enable spectrum logging if requested, as the spectrum app needs to be loaded
if os.environ.get('SPECTRUM'):
    from spectrum.django import fire_hose, FIRE_HOSE_WS
    LOGGING = fire_hose(base_config=FIRE_HOSE_WS)
    LOGGING['root']['handlers'] = ['root']
