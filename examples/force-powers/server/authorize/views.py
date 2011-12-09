from urllib import urlencode

from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from scopes.models import Scope


from pauth.flows import auth_code as flow
from pauth.errors import OAuthError


def authorize(request):
    try:
        auth_request = flow.request_authorization(request)
    except OAuthError as e:
        return e.get_response()

    return request_authorization(request,
                                 auth_request.client,
                                 auth_request.scopes,
                                 auth_request.redirect_uri,
                                 auth_request.state)


def request_authorization(request, client, scopes, redirect_uri, state=None):
    context = {'form_action': '/authorize/response',
               'scopes': [s.description for s in scopes],
               'client_id': client.id,
               'client_name': client.name,
               'redirect_uri': redirect_uri}

    if state is not None:
        context['state'] = state

    return TemplateResponse(request, 'authorize.html', context)


def authorize_response(request):
    request_granted = request.GET.get('grant', '').lower() == 'true'
    redirect_uri = request.GET.get('redirect_uri')
    state = request.GET.get('state')
    parameters = {}

    if state is not None:
        parameters['state'] = state

    if request_granted:
        parameters['code'] = 'some-code'
    else:
        parameters['error'] = 'access_denied'

    uri = '{redirect_uri}?{query_string}'.format(
        redirect_uri=redirect_uri,
        query_string=urlencode(parameters))
    response = HttpResponseRedirect(uri)
    #response['Authorization'] = 'Basic ' + "a-public-client:don't-tell-anyone!".encode('base64')
    return response


def get_scope(id):
    try:
        scope = Scope.objects.get(id=id)
    except Scope.DoesNotExist:
        return None

    return scope
