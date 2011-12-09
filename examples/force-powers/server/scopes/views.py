from simplejson import dumps

from django.http import HttpResponse, HttpResponseNotFound

from clients.models import Client
from models import Scope


def get_all_scopes(request):
    scopes = Scope.objects.all().order_by('description')
    return HttpResponse(make_scopes_json(scopes),
                        content_type='application/json')


def get_client_scopes(request, client):
    try:
        client = Client.objects.get(id=client)
    except Client.DoesNotExist:
        return HttpResponseNotFound()

    return HttpResponse(make_scopes_json(client.allowed_scopes.all()),
                        content_type='application/json')


def make_scopes_json(scopes):
    scopes_dict = dict((scope.id, scope.description)
                      for scope in scopes)
    return dumps(scopes_dict)
