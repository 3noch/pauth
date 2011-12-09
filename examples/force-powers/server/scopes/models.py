from django.db import models


class Scope(models.Model):
    id = models.CharField(max_length=512, primary_key=True)
    description = models.CharField(max_length=1024)

    def __unicode__(self):
        return u'Scope "{scope.id}"'.format(scope=self)
