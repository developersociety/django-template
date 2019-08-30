from django.conf import settings
from django.forms.utils import ErrorList
from django.urls import Resolver404, resolve

from wagtail.core.blocks import (
    BooleanBlock,
    CharBlock,
    ChoiceBlock,
    PageChooserBlock,
    RawHTMLBlock,
    RichTextBlock,
    StreamBlock,
    StreamBlockValidationError,
    StructBlock,
    StructValue,
    URLBlock,
)
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock

from . import choices as page_choices


class BaseBlock(StructBlock):
    class Meta:
        form_classname = "full-width"
        form_template = "admin/blocks/base_block.html"


class AdvancedBlock(StructBlock):
    """
    Advanced fields must be declared after all other fields and the order of advanced_fields
    in class Meta must match the order of these.
    """

    class Meta:
        form_classname = "full-width"
        form_template = "admin/blocks/advanced_block.html"


class URLValue(StructValue):
    """
    Get active link used in LinkBlock or LinkButtonBlock if there is one
    """

    def get_url(self):
        link_to = self.get("link_to")

        if link_to == "page" or link_to == "file":
            # If file or page check obj is not None
            if self.get(link_to):
                return self.get(link_to).url
        elif link_to == "custom_url":
            return self.get(link_to)
        return None


class LinkBlock(BaseBlock):
    """
    Link chooser for [page/file/custom url], with validation on inputted links.
    Extended as a button block in LinkButtonBlock, and used for choosing links in other blocks
    This block is for inhertiance only, not to be added to StreamFields, hence no template required
    """

    link_to = ChoiceBlock(
        choices=[("page", "Page"), ("file", "File"), ("custom_url", "Custom URL")], required=False
    )
    page = PageChooserBlock(required=False)
    file = DocumentChooserBlock(required=False)
    custom_url = URLBlock(required=False)
    new_window = BooleanBlock(label="Open page in a new tab", required=False)

    class Meta:
        label = None
        value_class = URLValue
        icon = "fa-share-square"
        form_classname = "full-width"
        form_template = "admin/blocks/link_block.html"

    def set_name(self, name):
        """
        Override StructBlock set_name so label can remain empty in streamblocks
        """
        self.name = name

    def clean(self, value):
        clean_values = super().clean(value)
        errors = {}

        url_default_values = {"page": None, "file": None, "custom_url": ""}
        url_type = clean_values.get("link_to")

        # Check that a value has been uploaded for the chosen link type
        if url_type != "" and clean_values.get(url_type) in [None, ""]:
            errors[url_type] = ErrorList(
                ["A {} link is required here".format(url_type.replace("_", " "))]
            )
        else:
            try:
                # Remove values added for link types not selected
                url_default_values.pop(url_type, None)
                for field in url_default_values:
                    clean_values[field] = url_default_values[field]
                # Valid custom_url by checking for 404 error
                if url_type == "custom_url" and not settings.DEBUG:
                    custom_url = clean_values.get("custom_url")
                    try:
                        resolve(custom_url)
                    except Resolver404:
                        errors[url_type] = ErrorList(
                            ["This page does not exist / returns a 404 error."]
                        )
            except KeyError:
                errors[url_type] = ErrorList(["Enter a valid link type."])

        if errors:
            raise StreamBlockValidationError(block_errors=errors)

        return clean_values


class LinkButtonBlock(LinkBlock):
    button_text = CharBlock(default="Read more", help_text="The text shown on the button.")
    style = ChoiceBlock(choices=page_choices.BUTTON_STYLES, default=page_choices.BUTTON_PRIMARY)

    class Meta:
        label = "Button"
        template = "blocks/link_button_block.html"
        form_template = "admin/blocks/link_button_block.html"


class RichTextEditorBlock(BaseBlock):
    content = RichTextBlock(
        features=[
            "h2",
            "h3",
            "h4",
            "h5",
            "bold",
            "italic",
            "align_left",
            "align_center",
            "align_right",
            "pre",
            "blockquote",
            "ol",
            "ul",
            "hr",
            "image",
            "link",
            "document-link",
        ]
    )

    class Meta:
        icon = "pilcrow"
        template = "blocks/richtext_block.html"


class HTMLBlock(BaseBlock):
    html_code = RawHTMLBlock()

    class Meta:
        icon = "code"
        template = "blocks/html_block.html"


class EmbedBlock(BaseBlock):
    """
    This block takes an embed URL and creates the associated iframe / embed element
    Videos should be uploaded using this block only, format: https://www.youtube.com/watch?v=<id>
    """

    embed_url = EmbedBlock(
        help_text="URL with the associated embed content. E.g. for YouTube videos,"
        "https://www.youtube.com/watch?v=<video_id>"
    )

    class Meta:
        icon = "media"
        template = "blocks/embed_block.html"


class ImageBlock(BaseBlock):
    image = ImageChooserBlock()
    caption = CharBlock(required=False, help_text="Optional caption shown below the image.")
    link = LinkBlock(
        required=False, help_text="Optional link to redirect/download when the image is clicked."
    )

    class Meta:
        icon = "image"
        template = "blocks/image_block.html"


class ColumnStreamBlock(StreamBlock):
    text = RichTextEditorBlock()
    button = LinkButtonBlock()
    image = ImageBlock()
    embed = EmbedBlock()
    html = HTMLBlock()

    class Meta:
        icon = "fa-align-left"


class TwoColumnBlock(BaseBlock):
    full_width_intro = RichTextBlock(required=False)
    background_colour = ChoiceBlock(
        choices=page_choices.BACKGROUND_COLORS, default=page_choices.NONE
    )
    alignment = ChoiceBlock(choices=page_choices.COLUMN_ALIGNMENTS, default=page_choices.HALVES)
    left_column = ColumnStreamBlock(
        min_num=0, help_text="Content displayed in left column, or top on mobile."
    )
    right_column = ColumnStreamBlock(
        min_num=0, help_text="Content displayed in right column, or bottom on mobile."
    )

    class Meta:
        icon = "fa-columns"
        form_template = "admin/blocks/column_block.html"
        template = "blocks/two_column_block.html"
        global_fields = ["full_width_intro", "background_colour", "alignment"]


class BaseStreamBlock(StreamBlock):
    text = RichTextEditorBlock()
    button = LinkButtonBlock()
    image = ImageBlock()
    embed = EmbedBlock()
    two_column_content = TwoColumnBlock()
    html = HTMLBlock()
