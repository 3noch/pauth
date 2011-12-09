from django.db import models

from scopes.models import Scope


class RedirectUri(models.Model):
    uri = models.CharField(max_length=1024)

    def __unicode__(self):
        return u'Redirection URI "{uri.uri}"'.format(uri=self)


class Client(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=512)
    secret = models.CharField(max_length=64)
    is_public = models.BooleanField()
    allowed_scopes = models.ManyToManyField(Scope)
    redirect_uris = models.ManyToManyField(RedirectUri)

    def __unicode__(self):
        return u'Client "{client.name}"'.format(client=self)
