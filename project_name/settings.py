"""
Django settings for {{ project_name }} project.

For more information on this file, see
https://docs.djangoproject.com/en/{{ docs_version }}/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Production / development switches
# https://docs.djangoproject.com/en/{{ docs_version }}/howto/deployment/checklist/

DEBUG = 'DEBUG' in os.environ

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(' ')

SECRET_KEY = os.environ.get('SECRET_KEY')


# Email
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#email

ADMINS = (
    ('Blanc Ltd', 'studio@blanc.ltd.uk'),
)

MANAGERS = ADMINS

SERVER_EMAIL = '{{ project_name }}@blanctools.com'

DEFAULT_FROM_EMAIL = '{{ project_name }}@blanctools.com'

EMAIL_SUBJECT_PREFIX = '[{{ project_name }}] '


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'raven.contrib.django.raven_compat',
    'blanc_basic_assets',
    'blanc_basic_news',
    'mptt',
    'django_mptt_admin',
    'blanc_basic_pages',
    'blanc_basic_events',
    'easy_thumbnails',
    'djangochurch_data',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'blanc_basic_pages.middleware.PageFallbackMiddleware',
)

ROOT_URLCONF = '{{ project_name }}.urls'

WSGI_APPLICATION = '{{ project_name }}.wsgi.application'


# Database
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#databases

import dj_database_url
DATABASES = {
    'default': dj_database_url.config(),
}


# Caches
# https://docs.djangoproject.com/en/{{ docs_version }}/topics/cache/

CACHES = {}
if os.environ.get('MEMCACHED_SERVERS'):
    CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': os.environ['MEMCACHED_SERVERS'].split(' '),
        'KEY_PREFIX': os.environ.get('MEMCACHED_PREFIX'),
    }
else:
    CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }


# Internationalization
# https://docs.djangoproject.com/en/{{ docs_version }}/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/London'

USE_I18N = False

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/{{ docs_version }}/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'htdocs/static')

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'theme/static'),
)


# File uploads
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#file-uploads

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'htdocs/media')

DEFAULT_FILE_STORAGE = os.environ.get(
    'DEFAULT_FILE_STORAGE', 'django.core.files.storage.FileSystemStorage')


# Templates
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#templates

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, '{{ project_name }}/templates'),
    os.path.join(BASE_DIR, 'theme/templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)


# Logging
# https://docs.djangoproject.com/en/{{ docs_version }}/topics/logging/#configuring-logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    }
}


# Any other application config goes below here

# Sites framework
SITE_ID = 1

# Thumbnail generation
THUMBNAIL_SUBDIR = 'thumbs'
THUMBNAIL_PRESERVE_EXTENSIONS = ('png',)
THUMBNAIL_QUALITY = 100
THUMBNAIL_DEFAULT_STORAGE = os.environ.get('DEFAULT_FILE_STORAGE')
THUMBNAIL_CACHE_DIMENSIONS = True

# Cloud storage
from contentfiles.config import libcloud_providers
LIBCLOUD_PROVIDERS = libcloud_providers('{{ project_name }}')

# Pages
# PAGE_TEMPLATES = (
#     ('', 'Default'),
# )
# PAGE_SHOW_LOGIN = False

# News
NEWS_TITLE = 'Django Church'
# NEWS_PER_PAGE = 10
# NEWS_FEED_LIMIT = 10

# Calendar
EVENTS_CALENDAR_NAME = 'Django Church'
# EVENTS_CALENDAR_DESCRIPTION = 'Events Calendar'
# EVENTS_START_SUNDAY = True

# Local settings override
try:
    from .local_settings import *  # noqa
except ImportError:
    pass
