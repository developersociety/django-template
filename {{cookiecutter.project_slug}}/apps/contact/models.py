from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.core.fields import RichTextField, StreamField

from pages.blocks import BaseStreamBlock


class FormField(AbstractFormField):
    page = ParentalKey('ContactPage', on_delete=models.CASCADE, related_name='form_fields')


class ContactPage(AbstractEmailForm):
    intro = StreamField(
        BaseStreamBlock(required=False),
        help_text='This content will also appear on the thank you screen',
        blank=True,
        null=True
    )
    content = StreamField(BaseStreamBlock(required=False), blank=True, null=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        StreamFieldPanel('intro'),
        StreamFieldPanel('content'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address'),
                FieldPanel('to_address'),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    parent_page_types = ['pages.Homepage', 'pages.StandardPage']
