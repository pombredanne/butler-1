from django.db import models

# Create your models here.


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

    def __unicode__(self):
        return self.nodename
