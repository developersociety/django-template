from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

from wagtail.contrib.table_block.blocks import TableBlock as WagtailTableBlock
from wagtail.core.blocks import (
    BooleanBlock, CharBlock, ChoiceBlock, DecimalBlock, ListBlock, PageChooserBlock, RawHTMLBlock,
    RichTextBlock, StreamBlock, StructBlock, StructValue, URLBlock
)
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock as WagtailEmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class BaseBlock(StructBlock):

    class Meta:
        form_classname = 'full-width'
        form_template = 'admin/blocks/base_block.html'


class AdvancedBlock(StructBlock):
    """
    Advanced fields must be declared after all other fields and the order of advanced_fields
    in class Meta must match the order of these.
    """

    class Meta:
        form_classname = 'full-width'
        form_template = 'admin/blocks/advanced_block.html'


class CustomURLValue(StructValue):
    """
    Get active link used in CustomURL or CustomURLButton if there is one
    """

    def get_url(self):
        link_to = self.get('link_to')

        if link_to == 'page' or link_to == 'file_url':
            return self.get(link_to).url
        elif link_to == 'custom_url':
            return self.get(link_to)
        return None


class CustomURLBlock(StructBlock):
    link_to = ChoiceBlock(
        choices=[
            ('page', 'Page'),
            ('file_url', 'File'),
            ('custom_url', 'Custom URL'),
        ],
        required=False,
    )
    page = PageChooserBlock(required=False)
    file_url = DocumentChooserBlock(required=False)
    custom_url = URLBlock(required=False)
    new_window = BooleanBlock(label='Open in new window', required=False)

    class Meta:
        label = None
        value_class = CustomURLValue
        form_classname = 'full-width'
        form_template = 'admin/blocks/url_block.html'

    def set_name(self, name):
        """
        Override StructBlock set_name so label can remain empty in streamblocks
        """
        self.name = name

    def clean(self, value):
        clean_values = super().clean(value)
        errors = {}

        url_default_values = {
            'page': None,
            'file_url': None,
            'custom_url': '',
        }
        url_type = clean_values.get('link_to')

        # If malicious data sent and url_type is invalid return validation error
        if url_type is None:
            errors[url_type] = ErrorList(['Enter a valid link type'])
            raise ValidationError('Validation error in StructBlock', params=errors)

        # Check that a value has been uploaded for the chosen link type
        if url_type != '' and not clean_values.get(url_type):
            errors[url_type] = ErrorList([
                'You need to add a {} link'.format(url_type.replace('_', ' '))
            ])
        else:
            try:
                # Remove values added for link types not selected
                url_default_values.pop(url_type, None)
                for field in url_default_values:
                    clean_values[field] = url_default_values[field]
            except KeyError:
                errors[url_type] = ErrorList(['Enter a valid link type'])

        if errors:
            raise ValidationError('Validation error in StructBlock', params=errors)

        return clean_values


class CustomURLButtonBlock(CustomURLBlock):
    link_text = CharBlock(
        help_text='This is the text that will appear in the button',
        default='Read more',
    )


class ImageGridItemBlock(BaseBlock):
    image = ImageChooserBlock(required=True)
    description = CharBlock(
        required=False,
        help_text='Used as ALT text',
    )
    caption = CharBlock(
        required=False,
        help_text='Shown below the image',
    )

    class Meta:
        icon = 'image'
        form_classname = 'full-width'
        form_template = 'admin/blocks/list_item_block.html'
        template = 'blocks/image_block.html'


class ImageGridBlock(BaseBlock):
    images = ListBlock(ImageGridItemBlock(label='Grid image'), min_num=3, max_num=7)

    class Meta:
        icon = 'grip'
        template = 'blocks/image_grid_block.html'
        form_template = 'admin/blocks/list_block.html'


class BasicImageBlock(AdvancedBlock):
    image = ImageChooserBlock(required=True)
    description = CharBlock(
        required=False,
        help_text='Used as ALT text',
    )
    caption = CharBlock(
        required=False,
        help_text='Shown below the image',
    )

    # Advanced fields
    link = CustomURLBlock(required=False)

    class Meta:
        icon = 'image'
        template = 'blocks/image_block.html'
        advanced_fields = ['link']


class AdvancedImageBlock(AdvancedBlock):
    image = ImageChooserBlock(required=True)
    description = CharBlock(
        required=False,
        help_text='Used as ALT text',
    )
    caption = CharBlock(
        required=False,
        help_text='Shown below the image',
    )
    alignment = ChoiceBlock(
        choices=[
            ('center', 'Center'),
            ('full', 'Full width'),
        ],
        default='center',
        help_text='Selecting "center" will set the image width to the size of the text content'
    )
    link = CustomURLBlock(required=False)

    class Meta:
        icon = 'image'
        template = 'blocks/image_block_advanced.html'
        advanced_fields = ['alignment', 'link']


class BannerBlock(AdvancedBlock):
    image = ImageChooserBlock(required=True)
    headline = CharBlock(required=True)
    sub_headline = CharBlock(required=False)
    link = CustomURLButtonBlock(required=True)

    # Advanced fields
    overlay = BooleanBlock(
        help_text='Add an overlay to darken the image for legibility',
        required=False,
    )
    overlay_opacity = DecimalBlock(
        help_text='Decimal representing the percentage of opacity—a higher number will be darker',
        decimal_places=2,
        max_digits=3,
        min_value=0.10,
        max_value=1.00,
        default=0.8,
    )

    class Meta:
        icon = 'image'
        template = 'blocks/banner_block.html'
        advanced_fields = ['overlay', 'overlay_opacity']


class CallToActionBlock(BaseBlock):
    text = CharBlock(required=True)
    link = CustomURLBlock(label=False)

    class Meta:
        icon = 'link'
        template = 'blocks/call_to_action_block.html'


class FileDownloadBlock(BaseBlock):
    file = DocumentChooserBlock()
    description = CharBlock(required=False)
    button_only = BooleanBlock(
        help_text='If checked this block will only show a button',
        required=False,
    )

    class Meta:
        icon = 'download'
        template = 'blocks/file_download_block.html'


class HTMLBlock(BaseBlock):
    code = RawHTMLBlock(label='html')

    class Meta:
        template = 'blocks/html_block.html'


class EmbedBlock(BaseBlock):
    url = WagtailEmbedBlock()
    alignment = ChoiceBlock(
        choices=[
            ('center', 'Center'),
            ('full', 'Full width'),
        ],
        default='center',
        help_text='Selecting "center" will set the image width to the size of the text content'
    )

    class Meta:
        template = 'blocks/embed_block.html'


class TableBlock(BaseBlock):
    table = WagtailTableBlock()

    class Meta:
        template = 'blocks/table_block.html'


class RichTextEditorBlock(BaseBlock):
    content = RichTextBlock(
        features=[
            'h1',
            'h2',
            'h3',
            'h4',
            'h5',
            'bold',
            'italic',
            'pre',
            'blockquote',
            'ol',
            'ul',
            'hr',
            'image',
            'link',
            'document_link',
        ]
    )

    class Meta:
        icon = 'pilcrow'
        template = 'blocks/richtext_block.html'


class ColumnStreamBlock(StreamBlock):
    text = RichTextEditorBlock()
    call_to_action = CallToActionBlock()
    image = BasicImageBlock()
    embed = EmbedBlock(icon='link')
    html = HTMLBlock(icon='code')


class TwoColumnBlock(BaseBlock):
    left_column = ColumnStreamBlock(min_num=1)
    right_column = ColumnStreamBlock(min_num=1)

    class Meta:
        icon = 'fa-columns'
        form_template = 'admin/blocks/column_block.html'
        template = 'blocks/two_column_block.html'


class BaseStreamBlock(StreamBlock):
    text = RichTextEditorBlock()
    call_to_action = CallToActionBlock()
    file_download = FileDownloadBlock()
    image = AdvancedImageBlock()
    image_grid = ImageGridBlock()
    banner = BannerBlock()
    table = TableBlock(icon='table')
    embed = EmbedBlock(icon='form')
    html = HTMLBlock(icon='code')
    two_column = TwoColumnBlock()
