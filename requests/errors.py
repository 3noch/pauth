from pauth.errors import OAuthError


class RequestError(OAuthError):
    """
    A base exception class for all errors having to do with OAuth requests.
    """
    id = 'invalid_request'

    def __init__(self, request):
        self.request = request

    def __repr__(self):
        return 'Invalid request'


class AccessDeniedError(RequestError):
    id = 'access_denied'

    def __repr__(self):
        return 'Request was denied'


class InvalidAccessTokenRequestError(RequestError):
    def __repr__(self):
        return 'Invalid request for an access token'


class InvalidAuthorizationRequestError(RequestError):
    def __repr__(self):
        return 'Invalid authorization request'


class UnsupportedResponseTypeError(RequestError):
    id = 'unsupported_response_type'

    def __repr__(self):
        return 'Unsupported response type: {response_type}'.format(
            response_type=self.request.response_type or '[empty]')


class UnknownAuthenticationMethod(RequestError):
    def __init__(self, method):
        self.method = method

    def __repr__(self):
        return 'Unknown authentication method: {method}'.format(method=self.method)


class MalformedAuthenticationCredentials(RequestError):
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return 'Malformed authentication credentials: {data}'.format(data=self.data)
