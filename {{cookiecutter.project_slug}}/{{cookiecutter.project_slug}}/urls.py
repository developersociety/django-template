from django.apps import apps
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponseServerError
from django.template import TemplateDoesNotExist, loader
{%- if cookiecutter.wagtail == 'y' %}

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

# from search import views as search_views
{%- endif %}

admin.site.site_title = '{{ cookiecutter.project_name }}'
admin.site.site_header = '{{ cookiecutter.project_name }}'

urlpatterns = [
{%- if cookiecutter.wagtail == 'y' %}
    url(r'^django-admin/', admin.site.urls),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
{%- else %}
    url(r'^admin/', admin.site.urls),
{%- endif %}
]

# Make it easier to see a 404 page under debug
if settings.DEBUG:
    from django.views.defaults import page_not_found

    urlpatterns += [
        url(r'^404/$', page_not_found, {'exception': None}),
    ]

# Only enable debug toolbar if it's an installed app
if apps.is_installed('debug_toolbar'):
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

# Serving static/media under debug
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
{%- if cookiecutter.wagtail == 'y' %}

# Wagtail catch-all
urlpatterns += [
    url(r'', include(wagtail_urls)),
]

{%- endif %}


def handler500(request, template_name='500.html'):
    """ 500 handler with request context. """
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return HttpResponseServerError('<h1>Server Error (500)</h1>', content_type='text/html')
    return HttpResponseServerError(template.render({
        'request': request,
    }))
