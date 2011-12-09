from urllib import urlencode

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from confidential.responses import NoCodeResponse
from shared.scopes import get_scopes


def home(request):
    return TemplateResponse(request, 'request-access.html', {
        'public': True,
        'form_action': 'authorize/',
        'all_scopes': get_scopes(),
        'client_scopes': get_scopes(settings.PUBLIC_CLIENT_ID),
        'client_id': settings.PUBLIC_CLIENT_ID,
        'state': 'somestate'})


def authorize(request):
    return HttpResponseRedirect(
        'http://{authorize_host}/authorize/?{query_string}'.format(
            authorize_host=settings.AUTHORIZATION_HOST,
            query_string=urlencode({
                'response_type': 'code',
                'client_id': settings.PUBLIC_CLIENT_ID,
                'redirect_uri': request.build_absolute_uri(reverse(authorize_response)),
                'scope': ' '.join(request.GET.getlist(u'scope')),
                'state': 'randomstate'})))



def authorize_response(request):
    error = request.GET.get('error')
    code = request.GET.get('code')

    if error is not None:
        if error.lower() == 'access_denied':
            return TemplateResponse(request, 'denied.html', {})
        else:
            return TemplateResponse(request, 'error.html', {
                'error': request.GET.get('error_description') or error})

    if code is not None:
        return TemplateResponse(request, 'request-access-token.html', {
            'form_action': request.build_absolute_uri(reverse(access_token)),
            'code': code})
    else:
        return NoCodeResponse(request)


def access_token(request):
    code = request.GET.get('code')

    if code is None:
        return NoCodeResponse(request)

    raise NotImplementedError
