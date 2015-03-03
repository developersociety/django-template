# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import blanc_basic_assets.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '__first__'),
        ('assets', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarouselBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_block', models.ForeignKey(to='pages.ContentBlock', null=True, editable=False)),
            ],
            options={
                'verbose_name': 'carousel',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CarouselSlide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('link', models.URLField(blank=True)),
                ('link_text', models.CharField(max_length=100, blank=True)),
                ('position', models.PositiveSmallIntegerField(default=0, db_index=True)),
                ('carousel', models.ForeignKey(to='carouselblock.CarouselBlock')),
                ('image', blanc_basic_assets.fields.AssetForeignKey(to='assets.Image')),
            ],
            options={
                'ordering': ('position',),
            },
            bases=(models.Model,),
        ),
    ]
