import errors


class RequestParameter(object):
    NAME = None

    def __init__(self, name, expected_value=None, required=False, propagate=False):
        self.name = name
        self.expected_value = expected_value
        self.required = required
        self.propagate = propagate

    def get_from_request(self, request):
        return request.parameters.get(self.NAME)


class RedirectUriParameter(RequestParameter):
    NAME = 'redirect_uri'


class StateParameter(RequestParameter):
    NAME = 'state'


class ClientParameter(RequestParameter):
    NAME = 'client_id'

    def get_from_request(self, request):
        from pauth.conf import middleware

        client_id = request.parameters.get(self.NAME)
        client = middleware.assign_client(client_id or '')

        if client is None:
            raise errors.UnknownClientError(request, client_id)
        elif not middleware.client_is_registered(client):
            raise errors.UnknownClientError(request, client_id)

        return client


class ResponseTypeParameter(RequestParameter):
    NAME = 'response_type'

    def get_from_request(self, request):
        response_type = request.parameters.get(self.NAME)

        if response_type != self.value:
            raise errors.UnsupportedResponseTypeError(request)

        return response_type


class GrantTypeParameter(RequestParameter):
    NAME = 'grant_type'

    def get_from_request(self, request):
        grant_type = request.parameters.get(self.NAME)

        if grant_type != self.value:
            raise errors.UnsupportedGrantTypeError(request)

        return grant_type


class ScopeParameter(RequestParameter):
    NAME = 'scope'

    def get_from_request(self, request):
        from pauth.conf import middleware

        scopes = None

        scope_ids = {}
        if request.parameters.get(self.NAME):
            scope_ids = request.parameters[self.NAME].split(' ')
        else:
            raise errors.NoScopeError(request)

        for id in scope_ids:
            scope = middleware.get_scope(id)
            if scope is None:
                raise errors.UnknownScopeError(request, id)
            elif not middleware.client_has_scope(request.client, scope):
                raise errors.ScopeDeniedError(request, id)
            else:
                scopes.append(scope)

        return scopes


class CodeParameter(RequestParameter):
    NAME = 'code'
