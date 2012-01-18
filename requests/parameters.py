from pauth.requests import errors


class RequestParameter(object):
    NAME = None
    UNEXPECTED_VALUE_ERROR = errors.UnsupportedTypeError

    def __init__(self, expected_value=None, required=False, propagate=False):
        self.expected_value = expected_value
        self.required = required
        self.propagate = propagate

    def get_from_request(self, request):
        value = request.parameters.get(self.NAME)

        # This check is duplicated in each request's _validate_query_args() method.
        if self.required and value is None:
            raise errors.MissingQueryArgumentsError(request, self.NAME)

        if self.expected_value is not None and value != self.expected_value:
            raise self.UNEXPECTED_VALUE_ERROR(request, value)


class RedirectUriParameter(RequestParameter):
    NAME = 'redirect_uri'


class StateParameter(RequestParameter):
    NAME = 'state'


class ClientParameter(RequestParameter):
    NAME = 'client_id'

    def get_from_request(self, request):
        from pauth.conf import adapter

        client_id = request.parameters.get(self.NAME)
        client = adapter.get_client(client_id or '')

        if client is None:
            raise errors.UnknownClientError(request, client_id)
        elif not adapter.client_is_registered(client):
            raise errors.UnknownClientError(request, client_id)

        return client


class ResponseTypeParameter(RequestParameter):
    NAME = 'response_type'
    UNEXPECTED_VALUE_ERROR = errors.UnsupportedResponseTypeError


class GrantTypeParameter(RequestParameter):
    NAME = 'grant_type'
    UNEXPECTED_VALUE_ERROR = errors.UnsupportedGrantTypeError


class ScopeParameter(RequestParameter):
    NAME = 'scope'

    def get_from_request(self, request):
        from pauth.conf import adapter

        scopes = None

        scope_ids = {}
        if request.parameters.get(self.NAME):
            scope_ids = request.parameters[self.NAME].split(' ')
        else:
            raise errors.NoScopeError(request)

        for id in scope_ids:
            scope = adapter.get_scope(id)
            if scope is None:
                raise errors.UnknownScopeError(request, id)
            elif not adapter.client_has_scope(request.client, scope):
                raise errors.ScopeDeniedError(request, id)
            else:
                scopes.append(scope)

        return scopes


class CodeParameter(RequestParameter):
    NAME = 'code'
