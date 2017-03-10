"""
Django settings for {{ cookiecutter.project_slug }} project.

For more information on this file, see
https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/
"""

import os
import sys

import dj_database_url


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


# Production / development switches
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/howto/deployment/checklist/

DEBUG = False


SECRET_KEY = os.environ.get('SECRET_KEY')


# Email
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#email

ADMINS = (
    ('Blanc Ltd', 'studio@blanc.ltd.uk'),
)
MANAGERS = ADMINS


SERVER_EMAIL = '{{ cookiecutter.project_slug }}@blanctools.com'
DEFAULT_FROM_EMAIL = '{{ cookiecutter.project_slug }}@blanctools.com'
EMAIL_SUBJECT_PREFIX = '[{{ cookiecutter.project_slug }}] '


PROJECT_APPS_ROOT = os.path.join(BASE_DIR, 'apps')
sys.path.append(PROJECT_APPS_ROOT)


DEFAULT_APPS = [
    # These apps should come first to load correctly.
    'blanc_admin_theme',
    'core',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]


THIRD_PARTY_APPS = [
{%- if cookiecutter.glitter == 'y' %}
    'django_mptt_admin',
    'glitter',
    'glitter.assets',
    'glitter.blocks.banner',
    'glitter.blocks.form',
    'glitter.blocks.html',
    'glitter.blocks.image',
    'glitter.blocks.redactor',
    'glitter.blocks.video',
    'glitter.pages',
    'mptt',
{%- endif %}
    'raven.contrib.django.raven_compat',
{%- if cookiecutter.glitter == 'y' %}
    'sorl.thumbnail',
{%- endif %}
]


PROJECT_APPS = [
{%- if cookiecutter.glitter == 'y' %}
    'pages',
{%- endif %}
]


INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + PROJECT_APPS


MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
{%- if cookiecutter.glitter == 'y' %}
    'glitter.pages.middleware.PageFallbackMiddleware',
    'glitter.middleware.ExceptionMiddleware',
{%- endif %}
]

ROOT_URLCONF = '{{ cookiecutter.project_slug }}.urls'

WSGI_APPLICATION = '{{ cookiecutter.project_slug }}.wsgi.application'


# Database
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(),
}


# Caches
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/topics/cache/

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
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'

USE_I18N = False

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'htdocs/static')

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


# File uploads
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#file-uploads

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'htdocs/media')

DEFAULT_FILE_STORAGE = os.environ.get(
    'DEFAULT_FILE_STORAGE', 'django.core.files.storage.FileSystemStorage'
)


# Templates
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Logging
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/topics/logging/#configuring-logging

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


# Sites framework
SITE_ID = 1


# Cloud storage
CONTENTFILES_PREFIX = '{{ cookiecutter.project_slug }}'
CONTENTFILES_SSL = True


# Improved cookie security
CSRF_COOKIE_HTTPONLY = True
{%- if cookiecutter.glitter == 'y' %}

# Thumbnail generation
THUMBNAIL_PREFIX = 'thumbs/'
THUMBNAIL_PRESERVE_FORMAT = True
THUMBNAIL_QUALITY = 100

# Glitter
GLITTER_DEFAULT_BLOCKS = [
    ('glitter_redactor.Redactor', 'Text'),
    ('glitter_image.ImageBlock', 'Image'),
    ('glitter_html.HTML', 'HTML'),
]
{%- endif %}
