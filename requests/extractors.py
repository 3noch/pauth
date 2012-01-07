import errors


def extract_redirect_uri(request):
    request.redirect_uri = request.parameters.get('redirect_uri')

def extract_client(self):
    from pauth.conf import middleware

    client_id = request.parameters.get('client_id')
    request.client = middleware.get_client(client_id or '')

    if request.client is None:
        raise errors.UnknownClientError(request, client_id)
    elif not middleware.client_is_registered(self.client):
        raise errors.UnknownClientError(request, client_id)

def extract_response_type(request):
    request.response_type = request.parameters.get('response_type')

    if request.response_type != request.REQUIRED_RESPONSE_TYPE:
        raise errors.UnsupportedResponseTypeError(request)

def extract_grant_type(request):
    request.grant_type = request.parameters.get('grant_type')

    if request.grant_type != request.REQUIRED_GRANT_TYPE:
        raise errors.UnsupportedGrantTypeError(request)

def _extract_scopes(request):
    from pauth.conf import middleware

    scope_ids = {}
    if request.parameters.get('scope'):
        scope_ids = request.parameters['scope'].split(' ')
    else:
        raise errors.NoScopeError(request)

    for id in scope_ids:
        scope = middleware.get_scope(id)
        if scope is None:
            raise errors.UnknownScopeError(request, id)
        elif not middleware.client_has_scope(self.client, scope):
            raise errors.ScopeDeniedError(request, id)
        else:
            request.scopes.append(scope)
