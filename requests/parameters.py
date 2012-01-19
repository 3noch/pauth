from pauth.requests import errors


# Priorities are used to determine which OAuth parameters to parse first.
INSANELY_HIGH_PRIORITY = 0
HIGH_PRIORITY = 1
MEDIUM_PRIORITY = 2
LOW_PRIORITY = 3


class RequestParameter(object):
    NAME = None
    PRIORITY = LOW_PRIORITY
    UNEXPECTED_VALUE_ERROR = errors.UnsupportedTypeError

    def __init__(self, expected_value=None, required=False, propagate=False):
        self.expected_value = expected_value
        self.required = required
        self.propagate = propagate

    def get_from_request(self, request):
        value = request.query_args.get(self.NAME)

        # This check is duplicated in each request's _validate_query_args() method.
        if self.required and value is None:
            raise errors.MissingQueryArgumentsError(request, self.NAME)

        if self.expected_value is not None and value != self.expected_value:
            raise self.UNEXPECTED_VALUE_ERROR(request, value)


class RedirectUriParameter(RequestParameter):
    NAME = 'redirect_uri'
    PRIORITY = INSANELY_HIGH_PRIORITY


class StateParameter(RequestParameter):
    NAME = 'state'
    PRIORITY = HIGH_PRIORITY


class ClientParameter(RequestParameter):
    NAME = 'client_id'

    def get_from_request(self, request):
        from pauth.conf import adapter

        client_id = request.query_args.get(self.NAME)
        client = adapter.get_client(client_id or '')

        if client is None:
            raise errors.UnknownClientError(request, client_id)
        elif not adapter.client_is_registered(client):
            raise errors.UnknownClientError(request, client_id)

        return client


class ResponseTypeParameter(RequestParameter):
    NAME = 'response_type'
    PRIORITY = MEDIUM_PRIORITY
    UNEXPECTED_VALUE_ERROR = errors.UnsupportedResponseTypeError


class GrantTypeParameter(RequestParameter):
    NAME = 'grant_type'
    PRIORITY = MEDIUM_PRIORITY
    UNEXPECTED_VALUE_ERROR = errors.UnsupportedGrantTypeError


class ScopeParameter(RequestParameter):
    NAME = 'scope'

    def get_from_request(self, request):
        from pauth.conf import adapter

        scope_ids = {}
        if request.query_args.get(self.NAME):
            scope_ids = request.query_args[self.NAME].split(' ')
        else:
            raise errors.NoScopeError(request)

        scopes = {}
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
