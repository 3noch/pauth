from pauth.conf.errors import UnconfiguredError


class FlowAdapter(object):
    def _get_oauth_request(request_class, request):
        from pauth.conf import adapter
        return adapter.adapt_request(request_class, request)


class AuthorizationCodeFlowAdapter(FlowAdapter):
    def get_authorization_code(client, scopes, state=None):
        raise UnconfiguredError()

    def get_access_token(client, scopes, authorization_code, state=None):
        raise UnconfiguredError()

    def handle_authorization_request(request):
        from pauth.flows.auth_code import AuthorizationRequest

        try:
            self._get_oauth_request(AuthorizationRequest, request)
        except OAuthError as error:
            return error.get_response()

        authorization_code = self.get_authorization_code(oauth_request.client,
                                                         oauth_request.scopes
                                                         oauth_request.state)

        if not authorization_code:
            raise AccessDeniedError(request)



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



class ImplicitGrantFlowAdapter(FlowAdapter):
    pass
