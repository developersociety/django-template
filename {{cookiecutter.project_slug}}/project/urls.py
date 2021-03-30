from django.apps import apps
from django.conf import settings
{%- if cookiecutter.multilingual == "y" %}
from django.conf.urls.i18n import i18n_patterns
{%- endif %}
from django.conf.urls.static import static
{%- if cookiecutter.wagtail != "y" %}
from django.contrib import admin
{%- endif %}
from django.contrib.staticfiles.views import serve as staticfiles_serve
from django.urls import include, path
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from django.views.static import serve
{%- if cookiecutter.wagtail == "y" %}

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

{%- endif %}

from core.views import server_error

{%- if cookiecutter.wagtail != "y" %}

admin.site.site_title = "{{ cookiecutter.project_name }}"
admin.site.site_header = "{{ cookiecutter.project_name }}"

{%- endif %}

handler500 = server_error

{%- if cookiecutter.multilingual == "y" and cookiecutter.wagtail == "y" %}

# Multilingual Wagtail site
urlpatterns = i18n_patterns(
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
)

urlpatterns += [
    path("sitemap.xml", sitemap, name="sitemap"),
    path(
        "robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")
    ),
]

urlpatterns += i18n_patterns(path("", include(wagtail_urls)))

{%- elif cookiecutter.multilingual == "n" and cookiecutter.wagtail == "y" %}

# Standard Wagtail site
urlpatterns = [
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("sitemap.xml", sitemap, name="sitemap"),
    path(
        "robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")
    ),
]

{%- elif cookiecutter.multilingual == "y" and cookiecutter.wagtail == "n" %}

# Multilingual Django site
urlpatterns = [
    path(
        "robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")
    ),
]

urlpatterns = i18n_patterns(path("admin/", admin.site.urls))

{%- else %}

# Standard Django site
urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")
    ),
]

{%- endif %}

# Allow testing of all styles locally
if settings.DEBUG:
    urlpatterns += [path("demo-styles/", TemplateView.as_view(template_name="demo_styles.html"))]

# Make it easier to see a 404 page under debug
if settings.DEBUG:
    from django.views.defaults import page_not_found

    urlpatterns += [path("404/", page_not_found, {"exception": None})]

# Only enable debug toolbar if it's an installed app
if apps.is_installed("debug_toolbar"):
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]

# Serving static/media under debug
urlpatterns += static(settings.STATIC_URL, never_cache(staticfiles_serve))
urlpatterns += static(settings.MEDIA_URL, never_cache(serve), document_root=settings.MEDIA_ROOT)

# Wagtail catch-all
urlpatterns += [path("", include(wagtail_urls))]
