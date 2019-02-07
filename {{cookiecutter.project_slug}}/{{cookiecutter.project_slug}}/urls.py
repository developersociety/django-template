from django.apps import apps
from django.conf import settings
from django.conf.urls import include, url

{%- if cookiecutter.multilingual == 'y' %}
from django.conf.urls.i18n import i18n_patterns
{%- endif %}
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponseServerError
from django.template import TemplateDoesNotExist, loader
from django.views.generic import TemplateView
{%- if cookiecutter.wagtail == 'y' %}

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

{%- if cookiecutter.multilingual == 'y' %}

from pages.views import LanguageRedirectView
{%- endif %}
{%- endif %}

admin.site.site_title = '{{ cookiecutter.project_name }}'
admin.site.site_header = '{{ cookiecutter.project_name }}'

urlpatterns = [
    url(
        r'^robots\.txt$',
        TemplateView.as_view(template_name='robots.txt', content_type='text/plain'),
    ),
]

{%- if cookiecutter.multilingual == 'y' and cookiecutter.wagtail == 'y' %}
# Multilingual wagtail site

urlpatterns = i18n_patterns()

urlpatterns += [
    url(r'^$', LanguageRedirectView.as_view(), name='language-redirect'),
    url(r'^django-admin/', admin.site.urls),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^sitemap\.xml$', sitemap, name='sitemap'),
]

# Wagtail catch-all
urlpatterns += [
    url(r'', include(wagtail_urls)),
]

{%- elif cookiecutter.multilingual == 'n' and cookiecutter.wagtail == 'y' %}
# Standard wagtail site

urlpatterns += [
    url(r'^django-admin/', admin.site.urls),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^sitemap\.xml$', sitemap, name='sitemap'),
]

# Wagtail catch-all
urlpatterns += [
    url(r'', include(wagtail_urls)),
]

{%- elif cookiecutter.multilingual == 'y' and cookiecutter.wagtail == 'n' %}
# multilingual django site

urlpatterns += i18n_patterns(
    url(r'^admin/', admin.site.urls),
)
{%- else %}
# Standard django site

urlpatterns += [
    url(r'^admin/', admin.site.urls),
]

{%- endif %}

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
