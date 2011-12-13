from pauth.errors import OAuthError


# --- Generic request errors ---
class RequestError(OAuthError):
    """
    A base exception class for all errors having to do with OAuth requests.
    """
    id = 'invalid_request'

    def __init__(self, request=None):
        super(RequestError, self).__init__(
            state=None if request is None else request.state,
            redirect_uri=None if request is None else request.redirect_uri)
        self.request = request

    def __str__(self):
        return 'Invalid request'


class AccessDeniedError(RequestError):
    id = 'access_denied'

    def __str__(self):
        return 'Request was denied'


class InvalidAccessTokenRequestError(RequestError):
    def __str__(self):
        return 'Invalid request for an access token'


class InvalidAuthorizationRequestError(RequestError):
    def __str__(self):
        return 'Invalid authorization request'


class UnsupportedResponseTypeError(RequestError):
    id = 'unsupported_response_type'

    def __str__(self):
        return 'Unsupported response type: {response_type}'.format(
            response_type=self.request.response_type or '[empty]')


# -- Errors with request's authentication ---
class RequestAuthenticationError(RequestError):
    pass


class UnknownAuthenticationMethod(RequestAuthenticationError):
    def __init__(self, request=None, method='[unknown]'):
        super(UnknownAuthenticationMethod, self).__init__(request)
        self.method = method

    def __str__(self):
        return 'Unknown authentication method: {method}'.format(method=self.method)


class MalformedAuthenticationCredentials(RequestAuthenticationError):
    def __init__(self, request=None, data='[unknown]'):
        super(MalformedAuthenticationCredentials, self).__init__(request)
        self.data = data

    def __str__(self):
        return 'Malformed authentication credentials: {data}'.format(data=self.data)


# --- Errors with the client making the request ---
class RequestingClientError(OAuthError):
    """
    A base exception class for all OAuth errors having to do with clients.
    """
    id = 'invalid_client'
    description = 'Invalid client: {id}'

    def __init__(self, request, client_id):
        super(RequestingClientError, self).__init__(
            state=request.state,
            redirect_uri=request.redirect_uri)
        self.client_id = client_id

    def __str__(self):
        return self.description.format(
            id=self.client.id if self.client is not None else '[empty]')


class UnknownClientError(RequestingClientError):
    description = 'Unknown client: {id}'


class UnauthorizedClientError(RequestingClientError):
    id = 'unauthorized_client'
    description = 'Unauthorized client: {id}'


# --- Errors with the requested scopes ---
class RequestedScopeError(RequestError):
    """
    A base exception class for all errors having to do with OAuth scopes.
    """
    id = 'invalid_scope'
    description = 'Scope error: {scope}'

    def __init__(self, request, scope_id=None):
        super(RequestedScopeError, self).__init__(request=request)
        self.scope_id = scope_id

    def __str__(self):
        return self.description.format(scope=self.scope_id)


class NoScopeError(RequestedScopeError):
    description = 'No scope was requested'


class UnknownScopeError(RequestedScopeError):
    description = 'Unknown scope: {scope}'


class ScopeDeniedError(RequestedScopeError):
    description = 'Access to scope was denied: {scope}'
