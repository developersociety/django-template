# -*- coding: utf-8 -*-

from .base import *  # NOQA @UnusedWildImport


DEBUG = False

# Use cached templates in production
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)
