from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.views import serve as staticfiles_serve
from django.http import HttpResponseServerError
from django.template import TemplateDoesNotExist, loader
from django.urls import include, path
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from django.views.static import serve
{%- if cookiecutter.wagtail == 'y' %}

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

# from search import views as search_views
{%- endif %}

admin.site.site_title = '{{ cookiecutter.project_name }}'
admin.site.site_header = '{{ cookiecutter.project_name }}'

urlpatterns = [
{%- if cookiecutter.wagtail == 'y' %}
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('sitemap.xml', sitemap, name='sitemap'),
{%- else %}
    path('admin/', admin.site.urls),
{%- endif %}
    path(
        'robots.txt',
        TemplateView.as_view(template_name='robots.txt', content_type='text/plain'),
    ),
]

# Make it easier to see a 404 page under debug
if settings.DEBUG:
    from django.views.defaults import page_not_found

    urlpatterns += [
        path('404/', page_not_found, {'exception': None}),
    ]

# Only enable debug toolbar if it's an installed app
if apps.is_installed('debug_toolbar'):
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

# Serving static/media under debug
urlpatterns += static(settings.STATIC_URL, never_cache(staticfiles_serve))
urlpatterns += static(settings.MEDIA_URL, never_cache(serve), document_root=settings.MEDIA_ROOT)
{%- if cookiecutter.wagtail == 'y' %}

# Wagtail catch-all
urlpatterns += [
    path('', include(wagtail_urls)),
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
