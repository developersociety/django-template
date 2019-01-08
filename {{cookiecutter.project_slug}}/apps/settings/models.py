from django import forms
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, HelpPanel, StreamFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.fields import RichTextField, StreamField

from pages.blocks import CustomURLButtonBlock


@register_setting(icon='fa-paragraph')
class FooterText(BaseSetting):
    body = RichTextField(features=['bold', 'italic', 'link'])

    panels = [
        FieldPanel('body'),
    ]


@register_setting(icon='fa-list')
class FooterLinks(BaseSetting):
    links = StreamField([
        (
            'link', CustomURLButtonBlock(
                label='link',
                max_num=5,
                template='blocks/footer_link_block.html',
                form_template='admin/blocks/footer_link_block.html',
            )
        ),
    ])

    panels = [StreamFieldPanel('links')]


@register_setting(icon='code')
class HeaderHTML(BaseSetting):
    html = models.TextField('HTML', blank=True)

    panels = [
        FieldPanel('html', widget=forms.Textarea(attrs={'rows': 10})),
        HelpPanel(
            """
            Raw HTML added at the end of the HTML head on every page. Useful for Analytics
            snippets, meta content and social graph headers.
            """
        ),
    ]

    class Meta:
        verbose_name = 'HTML - Header'


@register_setting(icon='code')
class FooterHTML(BaseSetting):
    html = models.TextField('HTML', blank=True)

    panels = [
        FieldPanel('html', widget=forms.Textarea(attrs={'rows': 10})),
        HelpPanel(
            """
            Raw HTML added at the end of the HTML body on every page. Useful for additional
            JavaScript.
            """
        ),
    ]

    class Meta:
        verbose_name = 'HTML - Footer'


@register_setting
class SocialMediaSettings(BaseSetting):
    facebook = models.URLField(help_text='Your Facebook page URL', blank=True)
    twitter = models.URLField(help_text='Your Twitter page URL', blank=True)
    instagram = models.URLField(help_text='Your Instagram page URL', blank=True)
    youtube = models.URLField(help_text='Your YouTube channel URL', blank=True)
