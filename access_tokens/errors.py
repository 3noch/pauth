from pauth.errors import PauthError



class AccessTokenError(PauthError):
    DESCRIPTION = 'Access token error for field: {field_name}'

    def __init__(self, token_type, field_name):
        self.token_type = token_type
        self.field_name = field_name

    def __str__(self):
        return DESCRIPTION.format(
            token_type=self.token_type,
            field_name=self.field_name)


class UnknownAccessTokenField(AccessTokenError):
    DESCRIPTION = '"{token_type}" access token field must be a string: {field_name}'


class AccessTokenFieldIsNotStringError(AccessTokenError):
    DESCRIPTION = '"{token_type}" access token field must be a string: {field_name}'


class AccessTokenFieldIsRequiredError(AccessTokenError):
    DESCRIPTION = 'Cannot delete field from "{token_type}" access token: {field_name}'
