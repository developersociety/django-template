from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "core"
{%- if cookiecutter.wagtail == 'y' %}

    def ready(self):
        super().ready()
        from . import monkeypatch  # noqa
{%- endif %}
