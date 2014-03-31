# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BBCodeTag'
        db.create_table('precise_bbcode_bbcodetag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag_name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=20)),
            ('tag_definition', self.gf('django.db.models.fields.TextField')()),
            ('html_replacement', self.gf('django.db.models.fields.TextField')()),
            ('helpline', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
            ('display_on_editor', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('newline_closes', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('same_tag_closes', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('standalone', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('render_embedded', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('escape_html', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('replace_links', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('strip', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('swallow_trailing_newline', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('precise_bbcode', ['BBCodeTag'])


    def backwards(self, orm):
        # Deleting model 'BBCodeTag'
        db.delete_table('precise_bbcode_bbcodetag')


    models = {
        'precise_bbcode.bbcodetag': {
            'Meta': {'object_name': 'BBCodeTag'},
            'display_on_editor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'tag_name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '20'})
        }
    }

    complete_apps = ['precise_bbcode']