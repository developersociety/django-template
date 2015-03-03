# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwoColumnTextBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('left_column', models.TextField(blank=True)),
                ('right_column', models.TextField(blank=True)),
                ('content_block', models.ForeignKey(editable=False, null=True, to='pages.ContentBlock')),
            ],
            options={
                'verbose_name': 'two column text',
            },
            bases=(models.Model,),
        ),
    ]
