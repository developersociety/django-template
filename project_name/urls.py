from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from blanc_pages import block_admin

urlpatterns = [
    # Examples:
    # url(r'^$', '{{ project_name }}.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # Blanc pages block admin
    url(r'^blockadmin/', include(block_admin.site.urls)),

    # Accounts
    url(r'^accounts/', include('django.contrib.auth.urls')),

    # Person app
    url(r'^person/', include('handbook.person.urls', namespace='person')),

    # Files
    url(r'^file/', include('handbook.files.urls', namespace='files')),

    # Places
    url(r'^places/', include('handbook.places.urls', namespace='places')),

    # Groups
    url(r'^group/', include('handbook.groups.urls', namespace='groups')),

    # Abuse reports
    url(r'^report/', include('handbook.report.urls', namespace='report')),

    # Discussion threads
    url(r'^thread/', include('handbook.threads.urls', namespace='threads')),

    # Knowledge base
    url(r'^knowledge/', include('handbook.pages.urls', namespace='knowledge')),

    # Links
    url(r'^links/', include('handbook.links.urls', namespace='links')),

    # Search
    url(r'^search/', include('handbook.search.urls', namespace='search')),

    # Dashboard
    url(r'', include('handbook.dashboard.urls', namespace='dashboard')),
]

# Make it easier to see a 404 page under debug
if settings.DEBUG:
    from django.views.defaults import page_not_found

    urlpatterns += [
        url(r'^404/$', page_not_found),
    ]

# Serving static/media under debug
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
