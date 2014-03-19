from django.db import models
import graphite


class Dashboard(models.Model):
    name = models.CharField(max_length=200)
    panels = models.ManyToManyField('DashboardPanel')

    def __unicode__(self):
        return self.name


class DashboardPanel(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, null=True, blank=True)

    graphite_target = models.CharField(max_length=1000)

    warning_threshold = models.IntegerField(null=True, blank=True)
    error_threshold = models.IntegerField(null=True, blank=True)

    value_format = models.CharField(max_length=50, null=True, blank=True)
    url = models.CharField(max_length=500, null=True, blank=True)

    def is_warning(self):
        if self.warning_threshold is None:
            return False
        return self.get_value() >= self.warning_threshold

    def is_error(self):
        if self.error_threshold is None:
            return False
        return self.get_value() >= self.error_threshold

    def get_value(self):
        if not hasattr(self, '_value'):
            data = graphite.get_latest_value(self.graphite_target)
            if len(data) > 0:
                self._value = data.values()[0]
            else:
                self._value = 0

        return self._value

    def get_url(self):
        if self.url is not None:
            return self.url
        return graphite.get_graph_url(self.graphite_target)

    def get_value_display(self):
        value = self.get_value()
        if self.value_format is None or self.value_format == '':
            return str(value)
        return self.value_format % value

    def __unicode__(self):
        return self.name