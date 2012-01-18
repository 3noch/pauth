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

    * The `ID` field is a string specifying an OAuth error code.
    * The `get_response()` method returns an ErrorResponse that can be
      sent over HTTP as an OAuth-compliant response to the error.
    """
    ID = None

    def __init__(self, state=None, redirect_uri=None):
        """
        Initializes an OAuthError. The code that raises this error may
        provide a `state` and a `redirect_uri` that will be used to
        form the redirection response back to the client whose request
        caused the error.
        """
        self.state = state
        self.redirect_uri = redirect_uri

    def get_response(self):
        from pauth.conf import adapter
        return adapter.adapt_response(ErrorResponse(id=self.ID,
                                                    description=unicode(self),
                                                    state=self.state,
                                                    redirect_uri=self.redirect_uri))

    def __str__(self):
        return 'Generic OAuth error'
