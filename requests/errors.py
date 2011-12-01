from pauth.errors import OAuthError


class RequestError(OAuthError):
    """
    A base exception class for all errors having to do with OAuth requests.
    """
    id = 'invalid_request'

    def __init__(self, request, state=None, redirect_uri=None):
        super(RequestError, self).__init__(state=None,
                                           redirect_uri=redirect_uri)
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


class UnknownAuthenticationMethod(OAuthError):
    def __init__(self, method, state=None, redirect_uri=None):
        super(UnknownAuthenticationMethod, self).__init__(state=state,
                                                          redirect_uri=redirect_uri)
        self.method = method

    def __str__(self):
        return 'Unknown authentication method: {method}'.format(method=self.method)


class MalformedAuthenticationCredentials(OAuthError):
    def __init__(self, data, state=None, redirect_uri=None):
        super(MalformedAuthenticationCredentials, self).__init__(state=state,
                                                                 redirect_uri=redirect_uri)
        self.data = data

    def __str__(self):
        return 'Malformed authentication credentials: {data}'.format(data=self.data)
