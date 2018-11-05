import os

from .base import *  # noqa

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = True

DATABASES = {
    'default': {
{%- if cookiecutter.geodjango == 'y' %}
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
{%- else %}
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
{%- endif %}
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
{%- if cookiecutter.wagtail == 'y' %}
    'wagtail.contrib.styleguide',
{%- endif %}
]

# Gulp runserver
TEMPLATES[0]['OPTIONS']['context_processors'].append(
    'core.context_processors.browsersync',
)

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

    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ] + MIDDLEWARE

# Only enable spectrum logging if requested, as the spectrum app needs to be loaded
if os.environ.get('SPECTRUM'):
    from spectrum.django import fire_hose, FIRE_HOSE_WS
    LOGGING = fire_hose(base_config=FIRE_HOSE_WS)
    LOGGING['root']['handlers'] = ['root']

# Allow login with remote passwords, but downgrade/swap to crypt for password hashing speed
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.CryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]
{%- if cookiecutter.wagtail == 'y' %}

# Wagtail search - use Postgres unless DISABLE_ELASTICSEARCH is enabled with environment vars
# eg. DISABLE_ELASTICSEARCH=1 ./manage.py runserver
if not os.environ.get('DISABLE_ELASTICSEARCH'):
    INSTALLED_APPS += [
        'wagtail.contrib.postgres_search',
    ]

    WAGTAILSEARCH_BACKENDS = {
        'default': {
            'BACKEND': 'wagtail.contrib.postgres_search.backend',
        },
    }
{%- endif %}
