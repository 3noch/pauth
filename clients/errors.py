from pauth.errors import OAuthError


class ClientError(OAuthError):
    pass


class UnknownClientError(ClientError):
    pass


class UnauthorizedClientError(ClientError):
    pass
