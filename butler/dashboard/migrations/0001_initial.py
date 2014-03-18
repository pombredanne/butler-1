# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Dashboard'
        db.create_table(u'dashboard_dashboard', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'dashboard', ['Dashboard'])

        # Adding M2M table for field panels on 'Dashboard'
        m2m_table_name = db.shorten_name(u'dashboard_dashboard_panels')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dashboard', models.ForeignKey(orm[u'dashboard.dashboard'], null=False)),
            ('dashboardpanel', models.ForeignKey(orm[u'dashboard.dashboardpanel'], null=False))
        ))
        db.create_unique(m2m_table_name, ['dashboard_id', 'dashboardpanel_id'])

        # Adding model 'DashboardPanel'
        db.create_table(u'dashboard_dashboardpanel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('graphite_target', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal(u'dashboard', ['DashboardPanel'])


    def backwards(self, orm):
        # Deleting model 'Dashboard'
        db.delete_table(u'dashboard_dashboard')

        # Removing M2M table for field panels on 'Dashboard'
        db.delete_table(db.shorten_name(u'dashboard_dashboard_panels'))

        # Deleting model 'DashboardPanel'
        db.delete_table(u'dashboard_dashboardpanel')


    models = {
        u'dashboard.dashboard': {
            'Meta': {'object_name': 'Dashboard'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'panels': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dashboard.DashboardPanel']", 'symmetrical': 'False'})
        },
        u'dashboard.dashboardpanel': {
            'Meta': {'object_name': 'DashboardPanel'},
            'graphite_target': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['dashboard']