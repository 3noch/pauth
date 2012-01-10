from authorization import get_credentials_by_method
import errors
import parameters as params


def MakeOAuthRequest(cls, request):
    """
    A factory for generating Request objects from a library-user's request.
    This factory uses the global middleware configuration to call a adapter
    function defined by the library-user that converts their own requests
    into an OAuthRequest that our library will understand.
    """
    from pauth.conf import middleware
    return middleware.adapt_request(cls, request)


class RequestMetaclass(type):
    def __new__(cls, name, bases, attributes):
        pass


class Request(object):
    EXPECTED_PARAMETERS = []

    def __init__(self, method='GET', headers=None, parameters=None):
        """
        This constructor defines our internally-standard interface for creating a
        request. The library-user will have to define an adapter to transform their
        requests into this interface (see `__new__()` above). But this interface
        is pretty generic and straightforward, so it shouldn't be a problem.
        """
        self.method = method
        self.headers = headers or {}
        self.parameters = parameters or {}

    def has_header(self, header):
        """
        Returns `True` when `header` matches at least one of the requests headers
        without comparing case.
        """
        return any(header.lower() == h.lower() for h in self.headers)

    def get_header(self, header):
        """
        Returns the value of the request header that matches `header` (without
        comparing case) or `None` if there is no matching header.
        """
        return next((v for k, v in self.headers.items()
                     if k.lower() == header.lower()), None)

    def get_credentials(self):
        """
        Returns Credentials object created from the information provided in the HTTP
        `Authorization` header, or `None` if this information is absent or unrecognized.
        """
        auth_header = self.get_header('Authorization')

        if auth_header is None:
            return None

        try:
            method, data = auth_header.split(' ', 1)
        except ValueError:
            return None

        try:
            return get_credentials_by_method(method.strip(), data.strip())
        except errors.UnknownAuthenticationMethod as error:
            # Intercept any errors raised when getting credentials and attach state and
            # redirection info for this request so that the error will generate the
            # correct response.
            raise self._propagate_error(error)

    def propagate(self, recipient):
        """
        Allows the request class to attach pertinent information to an error before it
        gets raised. This isn't just convenient but essential when the error needs to be
        sent to the requester via the redirect URI that was provided in the request. This
        method takes an error and returns a modified version of the error.
        """
        pass


class BaseAuthorizationRequest(Request):
    __metaclass__ = RequestMetaclass

    ALLOWED_METHOD = 'GET'
    ALLOWED_RESPONSE_TYPE = None

    redirect_uri = params.RedirectUriParameter(propagate=True)
    state = params.StateParameter(propagate=True)
    response_type = params.ResponseTypeParameter(required=True, value=ALLOWED_RESPONSE_TYPE)
    client = params.ClientParameter(name='client_id', required=True)
    scope = params.ScopeParameter()


class BaseAccessTokenRequest(Request):
    __metaclass__ = RequestMetaclass

    ALLOWED_METHOD = 'POST'
    ALLOWED_GRANT_TYPE = None

    redirect_uri = params.RedirectUriParameter(propagate=True)
    grant_type = params.GrantTypeParameter(required=True, value=ALLOWED_GRANT_TYPE)
    code = params.CodeParameter(required=True)
