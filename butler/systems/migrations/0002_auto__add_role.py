# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Role'
        db.create_table(u'systems_role', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal(u'systems', ['Role'])

        # Adding M2M table for field roles on 'Machine'
        m2m_table_name = db.shorten_name(u'systems_machine_roles')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('machine', models.ForeignKey(orm[u'systems.machine'], null=False)),
            ('role', models.ForeignKey(orm[u'systems.role'], null=False))
        ))
        db.create_unique(m2m_table_name, ['machine_id', 'role_id'])


    def backwards(self, orm):
        # Deleting model 'Role'
        db.delete_table(u'systems_role')

        # Removing M2M table for field roles on 'Machine'
        db.delete_table(db.shorten_name(u'systems_machine_roles'))


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
            'nodename': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['systems.Role']", 'null': 'True', 'blank': 'True'})
        },
        u'systems.role': {
            'Meta': {'object_name': 'Role'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['systems']