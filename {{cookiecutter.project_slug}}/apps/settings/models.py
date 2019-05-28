from django import forms
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, HelpPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting(icon="code")
class HeaderHTML(BaseSetting):
    html = models.TextField("HTML", blank=True)

    panels = [
        FieldPanel("html", widget=forms.Textarea(attrs={"rows": 10})),
        HelpPanel(
            """
            Raw HTML added at the end of the HTML head on every page. Useful for Analytics
            snippets, meta content and social graph headers.
            """
        ),
    ]

    class Meta:
        verbose_name = "HTML - Header"


@register_setting(icon="code")
class FooterHTML(BaseSetting):
    html = models.TextField("HTML", blank=True)

    panels = [
        FieldPanel("html", widget=forms.Textarea(attrs={"rows": 10})),
        HelpPanel(
            """
            Raw HTML added at the end of the HTML body on every page. Useful for additional
            JavaScript.
            """
        ),
    ]

    class Meta:
        verbose_name = "HTML - Footer"
