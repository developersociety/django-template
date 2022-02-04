from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('wagtailimages', '0001_squashed_0021'),
    ]

    operations = [
        migrations.CreateModel(
            name='StandardPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('share_description', models.TextField(blank=True, help_text='\n        Description/preview shown when this page is shared on social media.\n        ', max_length=150)),
                ('content', wagtail.core.fields.StreamField([('text', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('description', wagtail.core.blocks.CharBlock(help_text='Used as ALT text', required=False)), ('caption', wagtail.core.blocks.CharBlock(help_text='Shown below the image', required=False)), ('link', wagtail.core.blocks.URLBlock(required=False)), ('new_window', wagtail.core.blocks.BooleanBlock(label='Open link in new window', required=False))])), ('html', wagtail.core.blocks.RawHTMLBlock(label='HTML'))], blank=True)),
                ('share_image', models.ForeignKey(blank=True, help_text='\n        Image shown when this page is shared on social media.\n        ', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('share_description', models.TextField(blank=True, help_text='\n        Description/preview shown when this page is shared on social media.\n        ', max_length=150)),
                ('content', wagtail.core.fields.StreamField([('text', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), ('image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('description', wagtail.core.blocks.CharBlock(help_text='Used as ALT text', required=False)), ('caption', wagtail.core.blocks.CharBlock(help_text='Shown below the image', required=False)), ('link', wagtail.core.blocks.URLBlock(required=False)), ('new_window', wagtail.core.blocks.BooleanBlock(label='Open link in new window', required=False))])), ('html', wagtail.core.blocks.RawHTMLBlock(label='HTML'))], blank=True)),
                ('share_image', models.ForeignKey(blank=True, help_text='\n        Image shown when this page is shared on social media.\n        ', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
