from pauth.access_tokens import errors


class BaseAccessToken(dict):
    HTTP_AUTH_SCHEME = None
    OAUTH_TOKEN_TYPE = None
    FIELDS = None

    def __init__(self, *args, **kwargs):
        super(BaseAccessToken, self).__init__(*args, **kwargs)
        self['token_type'] = self.OAUTH_TOKEN_TYPE

    def __setitem__(self, key, value):
        if key in self.FIELDS:
            if isinstance(value, str) or isinstance(value, unicode):
                super(BaseAccessToken, self).__setitem__(key, value)
            else:
                raise errors.AccessTokenFieldIsNotStringError(self.HTTP_AUTH_SCHEME, key)
        else:
            raise errors.UnknownAccessTokenFieldError(self.HTTP_AUTH_SCHEME, key)

    def __delitem__(self, key):
        raise errors.AccessTokenFieldIsRequiredError(self.HTTP_AUTH_SCHEME, key)


class ExampleAccessToken(BaseAccessToken):
    HTTP_AUTH_SCHEME = 'Example'
    OAUTH_TOKEN_TYPE = HTTP_AUTH_SCHEME.lower()
    FIELDS = ['access_token']


class BearerAccessToken(BaseAccessToken):
    """
    Defines an OAuth Bearer Token as defined in the
    [IETF specification](http://tools.ietf.org/html/draft-ietf-oauth-v2-bearer)
    """
    HTTP_AUTH_SCHEME = 'Bearer'
    OAUTH_TOKEN_TYPE = HTTP_AUTH_SCHEME.lower()
    FIELDS = ['access_token']


class MacAccessToken(BaseAccessToken):
    HTTP_AUTH_SCHEME = 'MAC'
