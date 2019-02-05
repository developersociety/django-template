{%- if cookiecutter.multilingual == 'y' %}
from django.conf import settings
{%- endif %}

from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from .blocks import BaseStreamBlock


class StandardPage(Page):
    content = StreamField(BaseStreamBlock(), blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]

{%- if cookiecutter.multilingual == 'y' %}
class HomePage(Page):
    content = StreamField(BaseStreamBlock(), blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]

    language = models.CharField(
        choices=settings.LANGUAGES,
        max_length=5,
        validators=[validate_language],
        unique=True,
    )

    # only allow homepages to be added underneath root
    # root page is only valid instance of bare page class
    parent_page_types = ['wagtailcore.Page']

    content_panels = Page.content_panels + [
        StreamFieldPanel('hero'),
        FieldPanel('language'),
        StreamFieldPanel('content'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('content'),
    ]
{%- else %}
class HomePage(Page):
    content = StreamField(BaseStreamBlock(), blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]
{%- endif %}