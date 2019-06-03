from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from .blocks import BaseStreamBlock


class StandardPage(Page):
    content = StreamField(BaseStreamBlock(), blank=True)

    content_panels = Page.content_panels + [StreamFieldPanel("content")]

    share_description = models.TextField(
        blank=True,
        max_length=150,
        help_text="""
        Default message shown when a page from this site is shared on social media. This message can be
        changed per page, under the \'promote\' tab.
        """,
    )
    share_image = models.ForeignKey(
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

    # Promote panels
    promote_panels = Page.promote_panels + [
        MultiFieldPanel(
            [FieldPanel("share_description"), ImageChooserPanel("share_image")],
            "Social meta",
            classname="page-options-panel",
        )
    ]


class HomePage(Page):
    content = StreamField(BaseStreamBlock(), blank=True)

    content_panels = Page.content_panels + [StreamFieldPanel("content")]

    share_description = models.TextField(
        blank=True,
        max_length=150,
        help_text="""
        Default message shown when a page from this site is shared on social media. This message can be
        changed per page, under the \'promote\' tab.
        """,
    )
    share_image = models.ForeignKey(
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
    # Promote panels
    promote_panels = Page.promote_panels + [
        MultiFieldPanel(
            [FieldPanel("share_description"), ImageChooserPanel("share_image")],
            "Social meta",
            classname="page-options-panel",
        )
    ]
