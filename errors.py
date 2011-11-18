from responses import ErrorResponse


class PauthError(Exception):
    """
    A base exception class for all Pauth-related errors.
    """
    pass


class OAuthError(PauthError):
    """
    A base exception class for all OAuth-specific errors. OAuth errors
    always contain an ErrorResponse object that can be used as an HTTP
    response that follows the OAuth specification.

    * The `id` field is a string specifying an OAuth error code.
    * The `get_response()` method returns an ErrorResponse that can be
      sent over HTTP as an OAuth-compliant response to the error.
    """
    id = None

    def get_response(self):
        return ErrorResponse(id, unicode(self))

    def __repr__(self):
        return 'Generic OAuth error'
