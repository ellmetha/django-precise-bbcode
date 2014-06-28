# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import precise_bbcode.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BBCodeTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag_name', models.SlugField(unique=True, max_length=20, verbose_name='BBCode tag name')),
                ('tag_definition', models.TextField(verbose_name='Tag definition')),
                ('html_replacement', models.TextField(verbose_name='Replacement HTML code')),
                ('newline_closes', models.BooleanField(default=False, help_text='Set this option to force the closing of this tag after a newline', verbose_name='Newline closing')),
                ('same_tag_closes', models.BooleanField(default=False, help_text='Set this option to force the closing of this tag after the beginning of a similar tag', verbose_name='Same tag closing')),
                ('end_tag_closes', models.BooleanField(default=False, help_text='Set this option to force the closing of this tag after the end of another tag', verbose_name='End tag closing')),
                ('standalone', models.BooleanField(default=False, help_text='Set this option if this tag does not have a closing tag', verbose_name='Standalone tag')),
                ('transform_newlines', models.BooleanField(default=True, help_text='Set this option to convert any line break to the equivalent markup', verbose_name='Transform line breaks')),
                ('render_embedded', models.BooleanField(default=True, help_text='Set this option to force the tags embedded in this tag to be rendered', verbose_name='Render embedded tags')),
                ('escape_html', models.BooleanField(default=True, help_text='Set this option to escape HTML characters (<, >, and &) inside this tag', verbose_name='Escape HTML characters')),
                ('replace_links', models.BooleanField(default=True, help_text='Set this option to replace URLs with link markups inside this tag', verbose_name='Replace links')),
                ('strip', models.BooleanField(default=False, help_text='Set this option to strip leading and trailing whitespace inside this tag', verbose_name='Strip leading and trailing whitespace')),
                ('swallow_trailing_newline', models.BooleanField(default=False, help_text='Set this option to swallow the first trailing newline', verbose_name='Swallow trailing newline')),
                ('helpline', models.CharField(max_length=120, null=True, verbose_name='Help text for this tag', blank=True)),
                ('display_on_editor', models.BooleanField(default=True, verbose_name='Display on editor')),
            ],
            options={
                'verbose_name': 'BBCode tag',
                'verbose_name_plural': 'BBCode tags',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SmileyTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', precise_bbcode.fields.SmileyCodeField(unique=True, max_length=60, verbose_name='Smiley code', db_index=True)),
                ('image', models.ImageField(upload_to=b'precise_bbcode/smilies', verbose_name='Smiley icon')),
                ('image_width', models.PositiveIntegerField(null=True, verbose_name='Smiley icon width', blank=True)),
                ('image_height', models.PositiveIntegerField(null=True, verbose_name='Smiley icon height', blank=True)),
                ('emotion', models.CharField(max_length=100, null=True, verbose_name='Related emotion', blank=True)),
                ('display_on_editor', models.BooleanField(default=True, verbose_name='Display on editor')),
            ],
            options={
                'verbose_name': 'Smiley',
                'verbose_name_plural': 'Smilies',
            },
            bases=(models.Model,),
        ),
    ]
