import functools
import os
import time

from django.conf import settings

BROWSERSYNC_URL = 'http://{host}:{port}/browser-sync/browser-sync-client.js?t={time}'


@functools.lru_cache()
def browsersync_url(host):
    """
    Return the browsersync javascript URL for a given hostname, or None if disabled.

    Browsersync runs on a different port to Django, but we want requests to use the same hostname
    or IP. We use the `BROWSERSYNC_PORT` environment variable set by runserver and use that to
    construct the URL. A querystring is added to prevent caching, however as this is function is
    decorated with lru_cache - it'll be consistent for the duration of the process.

    Returns None if `BROWSERSYNC_PORT` isn't set (disabled).
    """
    port = os.environ.get('BROWSERSYNC_PORT')

    if port is None:
        return None

    cache_time = int(time.time())
    url = BROWSERSYNC_URL.format(host=host, port=port, time=cache_time)
    return url


def browsersync(request):
    """
    Add `BROWSERSYNC_URL` to the global template context.
    """
    host = request.get_host()
    if ':' in host:
        host, port = host.split(':')

    url = browsersync_url(host=host)

    return {
        'BROWSERSYNC_URL': url,
    }


def demo(request):
    return {
        'DEMO_SITE': settings.DEMO_SITE,
    }
