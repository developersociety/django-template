import dj_database_url

from .base import *  # noqa

# Tests are performed on a test_ database, however to avoid any connections/queries going to
# another database we also set this as the 'default' as well

{%- if cookiecutter.geodjango == 'y' %}
DATABASES = {"default": dj_database_url.config(default=f"postgis:///test_{PROJECT_SLUG}_django")}
{%- else %}
DATABASES = {"default": dj_database_url.config(default=f"postgres:///test_{PROJECT_SLUG}_django")}
{%- endif %}
DATABASES["default"]["TEST"] = {"NAME": DATABASES["default"]["NAME"]}

SECRET_KEY = "secret"

STATIC_ROOT = os.environ["STATIC_ROOT"]

INSTALLED_APPS += ["django_extensions"]

# Test Runner
# - Use XMLTestRunner for tox to output per test XML files
# - Output these to a separate directory to avoid clutter
TEST_RUNNER = "xmlrunner.extra.djangotestrunner.XMLTestRunner"
TEST_OUTPUT_DIR = "reports"

# Always run tests with the fastest password hasher
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Disable axes during testing
AXES_ENABLED = False
