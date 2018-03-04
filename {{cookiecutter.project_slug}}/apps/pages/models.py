from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from .blocks import BaseStreamBlock


class StandardPage(Page):
    content = StreamField(BaseStreamBlock(), blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]


class HomePage(Page):
    content = StreamField(BaseStreamBlock(), blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]
