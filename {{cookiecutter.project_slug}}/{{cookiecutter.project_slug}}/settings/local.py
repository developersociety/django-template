import os
from importlib import import_module

from .base import *  # noqa

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

INTERNAL_IPS = ['127.0.0.1']
ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'django_extensions',
]

# Gulp runserver
TEMPLATES[0]['OPTIONS']['context_processors'].append(
    'core.context_processors.browsersync',
)

# Add flat theme if module is installed.
try:
    import_module('flat')
except ImportError:
    pass
else:
    INSTALLED_APPS.insert(0, 'flat')

# Use vanilla StaticFilesStorage to allow tests to run outside of tox easily
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

SECRET_KEY = '{{ cookiecutter.project_slug }}'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Django debug toolbar - show locally unless DISABLE_TOOLBAR is enabled with environment vars
# eg. DISABLE_TOOLBAR=1 ./manage.py runserver
if not os.environ.get('DISABLE_TOOLBAR'):
    INSTALLED_APPS += [
        'debug_toolbar',
    ]

    MIDDLEWARE_CLASSES = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ] + MIDDLEWARE_CLASSES

# Only enable spectrum logging if requested, as the spectrum app needs to be loaded
if os.environ.get('SPECTRUM'):
    from spectrum.django import fire_hose, FIRE_HOSE_WS
    LOGGING = fire_hose(base_config=FIRE_HOSE_WS)
    LOGGING['root']['handlers'] = ['root']
