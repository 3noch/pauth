from pauth.errors import OAuthError


# --- Generic request errors ---
class RequestError(OAuthError):
    """
    A base exception class for all errors having to do with OAuth requests.
    """
    ID = 'invalid_request'
    DESCRIPTION = 'Invalid request'

    def __init__(self, request=None):
        super(RequestError, self).__init__(
            state=None if request is None else request.state,
            redirect_uri=None if request is None else request.redirect_uri)
        self.request = request

    def __str__(self):
        return self.DESCRIPTION.format(self=self)


class AccessDeniedError(RequestError):
    ID = 'access_denied'
    DESCRIPTION = 'Request was denied'


class AuthorizationRequestError(RequestError):
    DESCRIPTION = 'Invalid authorization request'


class AccessTokenRequestError(RequestError):
    DESCRIPTION = 'Invalid request for an access token'


class MissingQueryArgumentsError(RequestError):
    DESCRIPTION = 'Required query arguments are missing: "{self.missing_args}"'

    def __init__(self, request=None, missing_args=None):
        super(MissingQueryArgumentsError, self).__init__(request)
        self.missing_args = ','.join(missing_args)


class UnsupportedResponseTypeError(RequestError):
    ID = 'unsupported_response_type'
    DESCRIPTION = 'Unsupported response type: "{self.request.response_type}"'


class UnsupportedGrantTypeError(RequestError):
    DESCRIPTION = 'Unsupported grant type: "{self.request.grant_type}"'


# --- Errors with request's authentication ---
class RequestAuthenticationError(RequestError):
    pass


class UnknownAuthenticationMethod(RequestAuthenticationError):
    DESCRIPTION = 'Unknown authentication method: {self.method}'

    def __init__(self, request=None, method='[unknown]'):
        super(UnknownAuthenticationMethod, self).__init__(request)
        self.method = method


class MalformedAuthenticationCredentials(RequestAuthenticationError):
    DESCRIPTION = 'Malformed authentication credentials: {self.data}'

    def __init__(self, request=None, data='[unknown]'):
        super(MalformedAuthenticationCredentials, self).__init__(request)
        self.data = data


# --- Errors with the client making the request ---
class RequestingClientError(RequestError):
    """
    A base exception class for all OAuth errors having to do with clients.
    """
    ID = 'invalid_client'

    def __init__(self, request=None, client_id=None):
        super(RequestingClientError, self).__init__(request)
        self.client_id = client_id


class UnknownClientError(RequestingClientError):
    DESCRIPTION = 'Unknown client: "{self.client_id}"'


class UnauthorizedClientError(RequestingClientError):
    ID = 'unauthorized_client'
    DESCRIPTION = 'Unauthorized client: "{self.client_id}"'


# --- Errors with the requested scopes ---
class RequestedScopeError(RequestError):
    """
    A base exception class for all errors having to do with OAuth scopes.
    """
    ID = 'invalid_scope'


class NoScopeError(RequestedScopeError):
    DESCRIPTION = 'No scope was requested'


class UnknownScopeError(RequestedScopeError):
    DESCRIPTION = 'Unknown scope: "{self.scope_id}"'


class ScopeDeniedError(RequestedScopeError):
    DESCRIPTION = 'Access to scope was denied: "{self.scope_id}"'
