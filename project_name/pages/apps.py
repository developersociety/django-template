from django.apps import AppConfig


class PagesConfig(AppConfig):
    name = '{{ project_name }}.pages'
    label = '{{ project_name }}_pages'
    verbose_name = 'Pages'
