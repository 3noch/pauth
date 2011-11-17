from pauth.errors import OAuthError


class ScopeError(OAuthError):
    def __init__(self, scope):
        self.scope = scope

    def __repr__(self):
        return 'There was an error with scope "{scope}".'.format(scope=self.scope)


class UnknownScopeError(ScopeError):
    def __repr__(self):
        return 'Unknown scope: {scope}'.format(scope=self.scope)


class ScopeDeniedError(ScopeError):
    def __repr__(self):
        return 'Access to scope was denied: {scope}'.format(scope=self.scope)
