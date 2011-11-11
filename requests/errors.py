from pauth.errors import OAuthError


class RequestError(OAuthError):
    response = None


class AccessDeniedError(RequestError):
    pass


class InvalidAccessTokenRequestError(RequestError):
    pass


class InvalidAuthorizationRequestError(RequestError):
    pass


class InvalidScopeError(RequestError):
    pass


class UnsupportedResponseTypeError(RequestError):
    pass
