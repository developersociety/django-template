from django import forms
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, HelpPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.images.edit_handlers import ImageChooserPanel


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


@register_setting(icon="link")
class SocialAccounts(BaseSetting):
    facebook_url = models.URLField(
        blank=True,
        help_text="""
        The URL of your organisation\'s Facebook page. E.g.
        "https://www.facebook.com/organisation_name_or_id"
        """,
    )
    twitter_handle = models.TextField(
        blank=True, help_text='Organisation\'s main Twitter handle. E.g. "@orgname"'
    )

    panels = [FieldPanel("facebook_url"), FieldPanel("twitter_handle")]


@register_setting(icon="fa-share")
class ShareMeta(BaseSetting):
    default_share_description = models.TextField(
        blank=True,
        max_length=150,
        help_text="""
        Default message shown when a page from this site is shared on social media. This message
        can be changed per page, under the \'promote\' tab.
        """,
    )
    default_share_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
        help_text="""
        Default image shown when a page from this site is shared on social media. This image can be
        changed per page, under the \'promote\' tab.
        """,
    )

    panels = [FieldPanel("default_share_description"), ImageChooserPanel("default_share_image")]

    class Meta:
        verbose_name = "Social share text / image"
