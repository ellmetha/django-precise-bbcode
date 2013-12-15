# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TestMessage'
        db.create_table(u'test_messages_testmessage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'_bbcode_content_rendered', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('bbcode_content', self.gf('precise_bbcode.fields.BBCodeTextField')(no_rendered_field=True)),
        ))
        db.send_create_signal(u'test_messages', ['TestMessage'])


    def backwards(self, orm):
        # Deleting model 'TestMessage'
        db.delete_table(u'test_messages_testmessage')


    models = {
        u'test_messages.testmessage': {
            'Meta': {'object_name': 'TestMessage'},
            u'_bbcode_content_rendered': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'bbcode_content': ('precise_bbcode.fields.BBCodeTextField', [], {u'no_rendered_field': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['test_messages']