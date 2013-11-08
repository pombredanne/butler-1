from django.db import models

# Create your models here.


class Environment(models.Model):
    name = models.CharName(max_length=20, db_index=True)

    def __unicode__(self):
        return self.name


class Machine(models.Model):

    environment = models.ForeignKey(Environment)
