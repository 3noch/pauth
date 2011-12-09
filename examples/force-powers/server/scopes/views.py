from django.shortcuts import get_object_or_404

from clients.models import Client
from decorators import scopes_view
from models import Scope


@scopes_view
def get_all_scopes(request):
    return Scope.objects.all().order_by('description')


@scopes_view
def get_client_scopes(request, client):
    client = get_object_or_404(Client, id=client)
    return client.allowed_scopes.all()
