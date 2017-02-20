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


# Test Runner
# - Use XMLTestRunner for tox to output per test XML files
# - Output these to a separate directory to avoid clutter
TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
TEST_OUTPUT_DIR = 'reports'
