from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('content', wagtail.core.fields.StreamField([('text', wagtail.core.blocks.RichTextBlock(icon='fa-paragraph')), ('image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('description', wagtail.core.blocks.CharBlock(help_text='Used as ALT text', required=False)), ('caption', wagtail.core.blocks.CharBlock(help_text='Shown below the image', required=False)), ('link', wagtail.core.blocks.URLBlock(required=False)), ('new_window', wagtail.core.blocks.BooleanBlock(label='Open link in new window', required=False))])), ('html', wagtail.core.blocks.RawHTMLBlock(label='HTML'))], blank=True)),
                {%- if cookiecutter.multilingual == 'y' %}
                ('language', models.CharField(choices=[('en', 'English'), ('uni', 'Unicode Test')], default='en', max_length=5, unique=True)),
                {%- endif %}
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='StandardPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('content', wagtail.core.fields.StreamField([('text', wagtail.core.blocks.RichTextBlock(icon='fa-paragraph')), ('image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('description', wagtail.core.blocks.CharBlock(help_text='Used as ALT text', required=False)), ('caption', wagtail.core.blocks.CharBlock(help_text='Shown below the image', required=False)), ('link', wagtail.core.blocks.URLBlock(required=False)), ('new_window', wagtail.core.blocks.BooleanBlock(label='Open link in new window', required=False))])), ('html', wagtail.core.blocks.RawHTMLBlock(label='HTML'))], blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
