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

INTERNAL_IPS = (
    '127.0.0.1',
)

INSTALLED_APPS += [
    'django_extensions',
]


# Add flat theme if module is installed.
try:
    import_module('flat')
except ImportError:
    pass
else:
    INSTALLED_APPS.insert(0, 'flat')


# Django debug toolbar - always show locally unless DEBUG_TOOLBAR is turned off
# eg. DEBUG_TOOLBAR=0 ./manage.py runserver
def show_toolbar(request):
    if request.is_ajax():
        return False

    return os.environ.get('DEBUG_TOOLBAR', '1') == '1'

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE_CLASSES = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE_CLASSES

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': '{}.show_toolbar'.format(__name__),
}


SECRET_KEY = '{{ cookiecutter.project_slug }}'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Only enable spectrum logging if requested, as the spectrum app needs to be loaded
if os.environ.get('SPECTRUM'):
    from spectrum.django import fire_hose, FIRE_HOSE_WS
    LOGGING = fire_hose(base_config=FIRE_HOSE_WS)
    LOGGING['root']['handlers'] = ['root']
