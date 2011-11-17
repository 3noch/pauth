from pauth.errors import OAuthError


class ScopeError(OAuthError):
    pass


class UnknownScopeError(ScopeError):
    pass


class ScopeDeniedError(ScopeError):
    pass
