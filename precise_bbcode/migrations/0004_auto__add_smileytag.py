# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SmileyTag'
        db.create_table('precise_bbcode_smileytag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('precise_bbcode.fields.SmileyCodeField')(unique=True, max_length=60, db_index=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('image_width', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('image_height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('emotion', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('display_on_editor', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('precise_bbcode', ['SmileyTag'])


    def backwards(self, orm):
        # Deleting model 'SmileyTag'
        db.delete_table('precise_bbcode_smileytag')


    models = {
        'precise_bbcode.bbcodetag': {
            'Meta': {'object_name': 'BBCodeTag'},
            'display_on_editor': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'end_tag_closes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'escape_html': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'helpline': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'html_replacement': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'newline_closes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'render_embedded': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'replace_links': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'same_tag_closes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'standalone': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'strip': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'swallow_trailing_newline': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tag_definition': ('django.db.models.fields.TextField', [], {}),
            'tag_name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '20'}),
            'transform_newlines': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'precise_bbcode.smileytag': {
            'Meta': {'object_name': 'SmileyTag'},
            'code': ('precise_bbcode.fields.SmileyCodeField', [], {'unique': 'True', 'max_length': '60', 'db_index': 'True'}),
            'display_on_editor': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'emotion': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'image_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'image_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['precise_bbcode']