# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import precise_bbcode.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_bbcode_content_rendered', models.TextField(null=True, editable=False, blank=True)),
                ('bbcode_content', precise_bbcode.fields.BBCodeTextField(no_rendered_field=True, verbose_name='BBCode content')),
            ],
            options={
                'verbose_name': 'Test message',
                'verbose_name_plural': 'Test messages',
            },
            bases=(models.Model,),
        ),
    ]
