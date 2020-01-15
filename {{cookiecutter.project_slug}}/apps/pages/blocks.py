from django.forms.utils import ErrorList

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
    TextBlock,
    URLBlock,
)
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock


class URLValue(StructValue):
    """
    Get active link used in LinkBlock
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


class BaseBlock(StructBlock):
    class Meta:
        form_classname = "full-width"
        form_template = "admin/blocks/base_block.html"


# Link block for use in other blocks
class LinkBlock(BaseBlock):
    link_to = ChoiceBlock(
        choices=[("page", "Page"), ("file", "File"), ("custom_url", "Custom URL")], required=False
    )
    page = PageChooserBlock(required=False)
    file = DocumentChooserBlock(required=False)
    custom_url = URLBlock(required=False)
    new_window = BooleanBlock(label="Open in new window", required=False)

    class Meta:
        label = None
        value_class = URLValue
        icon = "fa-share-square"
        form_classname = "full-width"
        form_template = "admin/blocks/link_block.html"
        template = "blocks/link_block.html"

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
                ["You need to add a {} link".format(url_type.replace("_", " "))]
            )
        else:
            try:
                # Remove values added for link types not selected
                url_default_values.pop(url_type, None)
                for field in url_default_values:
                    clean_values[field] = url_default_values[field]
            except KeyError:
                errors[url_type] = ErrorList(["Enter a valid link type"])

        if errors:
            raise StreamBlockValidationError(block_errors=errors)

        return clean_values


class RichTextEditorBlock(BaseBlock):
    content = RichTextBlock(
        features=[
            "h2",
            "h3",
            "h4",
            "bold",
            "italic",
            "align_center",
            "blockquote",
            "ol",
            "ul",
            "hr",
            "image",
            "link",
            "document-link",
            "embed",
        ]
    )

    class Meta:
        icon = "pilcrow"
        template = "blocks/richtext_block.html"


class ColumnRichTextEditorBlock(BaseBlock):
    content = RichTextBlock(
        features=["h2", "h3", "h4", "bold", "italic", "ol", "ul", "hr", "link", "document-link"]
    )

    class Meta:
        icon = "pilcrow"
        template = "blocks/richtext_block.html"


class ImageBlock(BaseBlock):
    image = ImageChooserBlock(required=True)
    description = CharBlock(required=False, help_text="Used as ALT text")
    caption = CharBlock(required=False, help_text="Shown below the image")
    link = LinkBlock(required=False)

    class Meta:
        icon = "image"
        template = "blocks/image_block.html"


class TileBlock(BaseBlock):
    link = LinkBlock()
    title = CharBlock()
    image = ImageChooserBlock()
    summary = TextBlock(help_text="Short description of what is on the linked page")
    link_text = CharBlock(
        default="Read more", help_text="This is the text that will appear in the button"
    )

    class Meta:
        icon = "form"
        template = "blocks/tile_block.html"


class TileGridBlock(StructBlock):
    links = StreamBlock([("link", TileBlock(label="Link", icon="link"))], min_num=1)

    class Meta:
        icon = "fa-th-large"
        form_template = "admin/blocks/column_block.html"
        template = "blocks/tiles_grid_block.html"


class ButtonBlock(BaseBlock):
    link = LinkBlock()
    link_text = CharBlock()
    align = ChoiceBlock(
        choices=[("left", "Left"), ("center", "Center"), ("right", "Right")],
        default="left",
        help_text="For arabic pages left will be right aligned as language is rtl",
    )

    class Meta:
        icon = "link"
        template = "blocks/button_block.html"


class DownloadBlock(BaseBlock):
    file = DocumentChooserBlock()
    title = CharBlock()
    summary = RichTextBlock(features=["bold", "italic"], required=False)

    class Meta:
        icon = "fa-download"
        template = "blocks/download_block.html"


class HTMLBlock(BaseBlock):
    code = RawHTMLBlock(label="html")

    class Meta:
        icon = "code"
        label = "HTML"
        template = "blocks/html_block.html"


class QuoteBlock(BaseBlock):
    quote = TextBlock()
    citation = CharBlock()
    role = CharBlock(required=False)

    class Meta:
        icon = "fa-quote-left"
        template = "blocks/quote_block.html"


class ColumnStreamBlock(StreamBlock):
    text = ColumnRichTextEditorBlock()
    image = ImageBlock()
    tile = TileBlock()
    button = ButtonBlock()
    html = HTMLBlock(icon="code")

    class Meta:
        icon = "fa-align-left"


class TwoColumnBlock(StructBlock):
    column_one = ColumnStreamBlock(
        min_num=0,
        help_text="Content displayed in left column in ltr or right in rtl, or top on mobile.",
    )
    column_two = ColumnStreamBlock(
        min_num=0,
        help_text="Content displayed in right column in ltr or right in rtl, or bottom on mobile.",
    )

    class Meta:
        icon = "fa-columns"
        template = "blocks/two_column_block.html"
        form_template = "admin/blocks/column_block.html"


class BaseStreamBlock(StreamBlock):
    text = RichTextEditorBlock()
    image = ImageBlock()
    tiles = TileGridBlock()
    download = DownloadBlock()
    button = ButtonBlock()
    quote = QuoteBlock()
    two_column_block = TwoColumnBlock()
    html = HTMLBlock()
