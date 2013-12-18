# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Environment'
        db.create_table(u'systems_environment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
        ))
        db.send_create_signal(u'systems', ['Environment'])

        # Adding model 'Machine'
        db.create_table(u'systems_machine', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('environment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['systems.Environment'])),
            ('nodename', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal(u'systems', ['Machine'])


    def backwards(self, orm):
        # Deleting model 'Environment'
        db.delete_table(u'systems_environment')

        # Deleting model 'Machine'
        db.delete_table(u'systems_machine')


    models = {
        u'systems.environment': {
            'Meta': {'object_name': 'Environment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'})
        },
        u'systems.machine': {
            'Meta': {'object_name': 'Machine'},
            'environment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['systems.Environment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nodename': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['systems']