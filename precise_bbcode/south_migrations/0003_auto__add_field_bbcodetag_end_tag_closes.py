# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'BBCodeTag.end_tag_closes'
        db.add_column('precise_bbcode_bbcodetag', 'end_tag_closes',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'BBCodeTag.end_tag_closes'
        db.delete_column('precise_bbcode_bbcodetag', 'end_tag_closes')


    models = {
        'precise_bbcode.bbcodetag': {
            'Meta': {'object_name': 'BBCodeTag'},
            'display_on_editor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
        }
    }

    complete_apps = ['precise_bbcode']