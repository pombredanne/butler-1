from django.db import models
from django.core.cache import get_cache
import graphite


class Dashboard(models.Model):
    name = models.CharField(max_length=200)
    panels = models.ManyToManyField('DashboardPanel')

    def get_good_metrics_count(self):
        count = 0
        for panel in self.panels.all():
            if not panel.is_error() and not panel.is_warning():
                count += 1
        return count

    def get_warn_metrics_count(self):
        count = 0
        for panel in self.panels.all():
            if panel.is_warning() and not panel.is_error():
                count += 1
        return count

    def get_error_metrics_count(self):
        count = 0
        for panel in self.panels.all():
            if panel.is_error():
                count += 1
        return count

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

    def get_value(self, use_cache=True):

        cache_key = 'panel-%s' % self.id
        cache = get_cache('default')

        if use_cache:
            value = cache.get(cache_key)
            if value is not None:
                self._value = value
                return self._value

        if not hasattr(self, '_value'):
            try:
                data = graphite.get_latest_value(self.graphite_target)
            except graphite.GraphiteLoadError as e:
                # This is a gratuitous hack. The 'countSeries' metric is very useful for counting
                # "number of systems which X", but if no systems match, graphite errors rather than
                # return 0. This code catches that particular case and assumes a value of 0, as
                # attempting to duplicate the functionality of 'countSeries' with other functions
                # such as "sumSeries" did not work well enough - sumSeries would rely on all the data
                # points having exactly the same timestamp
                if e.status_code == 500 and 'countSeries' in self.graphite_target\
                   and 'reduce() of empty sequence with no initial value' in e.content:
                    self._value = 0
                else:
                    raise
            else:
                if len(data) > 0:
                    self._value = data.values()[0]
                else:
                    self._value = 0

        cache.set(cache_key, self._value)

        return self._value

    def get_url(self):
        if self.url is not None and self.url != '':
            return self.url
        return graphite.get_graph_url(self.graphite_target)

    def get_value_display(self):
        value = self.get_value()
        if self.value_format is None or self.value_format == '':
            return str(value)
        return self.value_format % value

    def __unicode__(self):
        return self.name