import warnings

from django.utils.deprecation import RemovedInDjango21Warning

import dj_database_url

from .base import *  # noqa

# Tests are performed on a test_ database, however to avoid any connections/queries going to
# another database we also set this as the 'default' as well
DATABASES = {
{%- if cookiecutter.geodjango == 'y' %}
    'default': dj_database_url.config(default='postgis:///test_{{ cookiecutter.project_slug }}_django'),
{%- else %}
    'default': dj_database_url.config(default='postgres:///test_{{ cookiecutter.project_slug }}_django'),
{%- endif %}
}
DATABASES['default']['TEST'] = {
    'NAME': DATABASES['default']['NAME'],
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

# Always error out on any warnings in loader_tags during testing with tox. This should highlight
# any problems with include tags missing templates.
warnings.filterwarnings(
    'error',
    category=RemovedInDjango21Warning,
    module=r'^django\.template\.loader_tags$',
)

# Always run tests with the fastest password hasher
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.CryptPasswordHasher',
]
{%- if cookiecutter.wagtail == 'y' %}

# Avoid wagtail search updates during testing
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.db',
    },
}
{%- endif %}
