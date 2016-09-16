from .base import *  # NOQA @UnusedWildImport


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DJANGO_DATABASE_NAME', '{{ cookiecutter.project_slug }}_django'),
        'USER': '',
        'PASSWORD': '',
        'PORT': '',
    },
}

SECRET_KEY = '{{ cookiecutter.project_slug }}'

STATIC_ROOT = os.environ['STATIC_ROOT']

INSTALLED_APPS += [
    'django_extensions',
]
