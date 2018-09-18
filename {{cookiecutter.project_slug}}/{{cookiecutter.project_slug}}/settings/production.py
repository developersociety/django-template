import os

import raven

from .base import *  # noqa

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(' ')

DEBUG = False

# Persistent database connections
if os.environ.get('DATABASE_CONN_MAX_AGE'):
    DATABASES['default']['CONN_MAX_AGE'] = int(os.environ.get('DATABASE_CONN_MAX_AGE'))

# Avoid server side cursors with pgbouncer
if os.environ.get('DATABASE_PGBOUNCER'):
    DATABASES['default']['DISABLE_SERVER_SIDE_CURSORS'] = True

# Use cached templates in production
TEMPLATES[0]['APP_DIRS'] = False
TEMPLATES[0]['OPTIONS']['loaders'] = [
    (
        'django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]
    ),
]

# SSL required for session/CSRF cookies
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Improve password security to a reasonable bare minimum
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Add more raven data to help diagnose bugs
RAVEN_CONFIG = {
    'release': raven.fetch_git_sha(BASE_DIR),
}

# Elastic APM
if os.environ.get('ELASTIC_APM_SERVER_URL'):
    INSTALLED_APPS += [
        'elasticapm.contrib.django.apps.ElasticAPMConfig',
    ]

    MIDDLEWARE = [
        'elasticapm.contrib.django.middleware.TracingMiddleware',
    ] + MIDDLEWARE

# Cache backed sessions for optimum performance
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
