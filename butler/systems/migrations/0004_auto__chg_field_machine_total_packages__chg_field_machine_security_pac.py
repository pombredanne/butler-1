# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Machine.total_packages'
        db.alter_column(u'systems_machine', 'total_packages', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Machine.security_packages'
        db.alter_column(u'systems_machine', 'security_packages', self.gf('django.db.models.fields.IntegerField')(null=True))

    def backwards(self, orm):

        # Changing field 'Machine.total_packages'
        db.alter_column(u'systems_machine', 'total_packages', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Machine.security_packages'
        db.alter_column(u'systems_machine', 'security_packages', self.gf('django.db.models.fields.IntegerField')())

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
            'last_update': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'nodename': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'requires_restart': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['systems.Role']", 'null': 'True', 'blank': 'True'}),
            'security_packages': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_packages': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'systems.role': {
            'Meta': {'object_name': 'Role'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['systems']