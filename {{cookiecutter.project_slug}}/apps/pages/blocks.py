from wagtail.core.blocks import (
    BooleanBlock,
    CharBlock,
    ChoiceBlock,
    RawHTMLBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    URLBlock,
)
from wagtail.images.blocks import ImageChooserBlock


class ImageBlock(StructBlock):
    image = ImageChooserBlock(required=True)
    description = CharBlock(required=False, help_text="Used as ALT text")
    caption = CharBlock(required=False, help_text="Shown below the image")
    link = URLBlock(required=False)
    new_window = BooleanBlock(label="Open link in new window", required=False)

    class Meta:
        icon = "image"
        template = "blocks/image_block.html"


class HeadingBlock(StructBlock):
    heading_text = CharBlock(form_classname="title", required=True)
    size = ChoiceBlock(
        choices=[("", "Select a header size"), ("h2", "H2"), ("h3", "H3"), ("h4", "H4")],
        blank=True,
        required=False,
    )

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"


class BaseStreamBlock(StreamBlock):
    text = RichTextBlock(icon="pilcrow")
    image = ImageBlock()
    html = RawHTMLBlock(label="HTML")
