from authorization import get_credentials_by_method
import errors
from pauth.clients.errors import UnauthorizedClientError, UnknownClientError
from pauth.scopes.errors import UnknownScopeError, ScopeDeniedError


def MakeOAuthRequest(cls, request):
    """
    A factory for generating Request objects from a library-user's request.
    This factory uses the global middleware configuration to call a adapter
    function defined by the library-user that converts their own requests
    into an OAuthRequest that our library will understand.
    """
    from pauth.conf import middleware
    return middleware.adapt_request(cls, request)


class Request(object):
    required_parameters = ()

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

        self.state = self.parameters.get('state')

    def _has_required_parameters(self):
        """
        A simple utility function for checking to see if the request has all
        the parameters defined in `required_parameters`. It's meant to be used by
        subclasses in order keep things DRY.
        """
        return all(r in self.parameters for r in self.required_parameters)

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

        try:
            method, data = auth_header.split(' ', 1)
        except (ValueError, AttributeError):
            return None

        try:
            return get_credentials_by_method(method.strip(), data.strip())
        except errors.UnknownAuthenticationMethod as e:
            # Intercept any errors raised when getting credentials and attach state and
            # redirection info for this request so that the error will generate the
            # correct response.
            e.state = self.state
            e.redirect_uri = self.redirect_uri
            raise e


class BaseAuthorizationRequest(Request):
    required_parameters = ('client_id', 'response_type')
    required_response_type = None

    def __init__(self, method='GET', headers=None, parameters=None):
        super(BaseAuthorizationRequest, self).__init__(method, headers, parameters)
        self.redirect_uri = None
        self.response_type = None
        self.client = None
        self.credentials = None
        self.scopes = {}
        self.redirect_uri = self.parameters.get('redirect_uri')

        if not self._has_required_parameters():
            raise errors.InvalidAuthorizationRequestError(self)

        self._extract_response_type()
        self._extract_client()
        self._extract_scopes()

    def _extract_response_type(self):
        self.response_type = self.parameters.get('response_type')

        if self.response_type != self.required_response_type:
            raise errors.UnsupportedResponseTypeError(self)

    def _extract_client(self):
        from pauth.conf import middleware

        client_id = self.parameters.get('client_id')
        self.client = middleware.get_client(client_id or '')
        self.credentials = self.get_credentials()

        if self.client is None:
            raise UnknownClientError(self, client_id)
        elif not middleware.client_is_registered(self.client):
            raise UnknownClientError(self, client_id)

    def _extract_scopes(self):
        from pauth.conf import middleware

        scope_ids = {}
        if 'scope' in self.parameters:
            scope_ids = self.parameters['scope'].split(' ')

        for id in scope_ids:
            scope = middleware.get_scope(id)
            if scope is None:
                raise UnknownScopeError(self, id)
            elif not middleware.client_has_scope(self.client, scope):
                raise ScopeDeniedError(self, id)
            else:
                self.scopes[id] = scope
