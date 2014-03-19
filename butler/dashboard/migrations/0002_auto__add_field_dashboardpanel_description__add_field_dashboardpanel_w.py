# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'DashboardPanel.description'
        db.add_column(u'dashboard_dashboardpanel', 'description',
                      self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True),
                      keep_default=False)

        # Adding field 'DashboardPanel.warning_threshold'
        db.add_column(u'dashboard_dashboardpanel', 'warning_threshold',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DashboardPanel.error_threshold'
        db.add_column(u'dashboard_dashboardpanel', 'error_threshold',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'DashboardPanel.description'
        db.delete_column(u'dashboard_dashboardpanel', 'description')

        # Deleting field 'DashboardPanel.warning_threshold'
        db.delete_column(u'dashboard_dashboardpanel', 'warning_threshold')

        # Deleting field 'DashboardPanel.error_threshold'
        db.delete_column(u'dashboard_dashboardpanel', 'error_threshold')


    models = {
        u'dashboard.dashboard': {
            'Meta': {'object_name': 'Dashboard'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'panels': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dashboard.DashboardPanel']", 'symmetrical': 'False'})
        },
        u'dashboard.dashboardpanel': {
            'Meta': {'object_name': 'DashboardPanel'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'error_threshold': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'graphite_target': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'warning_threshold': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['dashboard']