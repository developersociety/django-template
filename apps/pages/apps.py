from django.apps import AppConfig


class PagesConfig(AppConfig):
    name = 'pages'
    label = '{{ project_name }}_pages'
    verbose_name = 'Pages'
