from django.db import models
import graphite


class Dashboard(models.Model):
    name = models.CharField(max_length=200)
    panels = models.ManyToManyField('DashboardPanel')

    def __unicode__(self):
        return self.name


class DashboardPanel(models.Model):
    name = models.CharField(max_length=200)

    graphite_target = models.CharField(max_length=1000)

    def get_value(self):
        data = graphite.get_latest_value(self.graphite_target)
        return data.values()[0]

    def __unicode__(self):
        return self.name