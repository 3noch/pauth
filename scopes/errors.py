from pauth.errors import OAuthError


class ScopeError(OAuthError):
    """
    A base exception class for all errors having to do with OAuth scopes.
    """
    id = 'invalid_scope'
    description = 'Scope error: {scope}'

    def __init__(self, scope):
        self.scope = scope

    def __repr__(self):
        return self.description.format(scope=self.scope)


class UnknownScopeError(ScopeError):
    description = 'Unknown scope: {scope}'


class ScopeDeniedError(ScopeError):
    description = 'Access to scope was denied: {scope}'
