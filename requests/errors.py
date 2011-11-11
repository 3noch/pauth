from pauth.errors import OAuthError


class RequestError(OAuthError):
    pass


class InvalidAuthorizationRequestError(RequestError):
    pass
