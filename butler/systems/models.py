from django.db import models


class Environment(models.Model):
    name = models.CharField(max_length=20, db_index=True)

    def __unicode__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    def __unicode__(self):
        return self.name


class Machine(models.Model):

    environment = models.ForeignKey(Environment)
    nodename = models.CharField(max_length=50, db_index=True)
    roles = models.ManyToManyField(Role, blank=True, null=True)

    security_packages = models.IntegerField(default=0)
    total_packages = models.IntegerField(default=0)
    requires_restart = models.NullBooleanField(default=None)

    last_update = models.DateTimeField(null=True, blank=True)

    @property
    def hostname(self):
        return '%s.%s.akvo-ops.org' % (self.nodename, self.environment.name)

    def __unicode__(self):
        return self.hostname