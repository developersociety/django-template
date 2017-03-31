import raven

from .base import *  # noqa


ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(' ')

DEBUG = False


# Use cached templates in production
TEMPLATES[0]['APP_DIRS'] = False
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]


# SSL required for session/CSRF cookies
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


# Add more raven data to help diagnose bugs
RAVEN_CONFIG = {
    'release': raven.fetch_git_sha(BASE_DIR),
}
