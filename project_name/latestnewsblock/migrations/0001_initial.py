# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '__first__'),
        ('pages', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='LatestNewsBlock',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('category', models.ForeignKey(null=True, to='news.Category', on_delete=django.db.models.deletion.SET_NULL, blank=True)),
                ('content_block', models.ForeignKey(to='pages.ContentBlock', null=True, editable=False)),
            ],
            options={
                'verbose_name': 'latest news',
            },
            bases=(models.Model,),
        ),
    ]
