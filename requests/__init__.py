from authorization import get_credentials_by_method
import errors
from pauth.clients import Client
from pauth.clients.errors import UnauthorizedClientError, UnknownClientError
from pauth.conf import _middleware
from pauth.credentials import ClientCredentials


def OAuthRequest(request):
    """
    A factory for generating Request objects from a library-user's request.
    This factory uses the global middleware configuration to call a adapter
    function defined by the library-user that converts their own requests
    into an OAuthRequest that our library will understand.
    """
    return _middleware.adapt_request(request)


class Request(object):
    required_parameters = ()

    def __init__(self, method='GET', headers=None, parameters=None):
        """
        This constructor defines our internally-standard interface for creating a
        request. The library-user will have to define an adapter to transform their
        requests into this interface (see `__new__()` above). But this interface
        is pretty generic and straightforward, so it shouldn't be a problem.

        This constructor also does some initial parsing of the request to get
        OAuth-specific parameters. Various subclasses of this class will have
        different rules for how the request ought to look. Depending on those rules
        (defined in the `validate()` method), this constructor can throw errors.
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
        except ValueError:
            return None

        return get_credentials_by_method(method.strip(), data.strip())


class AuthorizationRequest(Request):
    required_parameters = ('client_id', 'response_type')

    def __init__(self, method='GET', headers=None, parameters=None):
        super(AuthorizationRequest, self).__init__(method, headers, parameters)

        if 'client_id' in self.parameters:
            credentials = ClientCredentials(self.parameters['client_id'],
                                            self.parameters.get('client_secret'))
            self.client = Client(credentials)
        else:
            self.client = None

        self.response_type = self.parameters.get('response_type')
        self.scope = self.parameters.get('scope')
        self.redirect_uri = self.parameters.get('redirect_uri')

        if not self._has_required_parameters():
            raise errors.InvalidAuthorizationRequestError(self)

        if self.client is None:
            raise UnknownClientError(self.client)
        elif not self.client.is_registered():
            raise UnknownClientError(self.client)
        elif not self.client.is_authorized():
            raise UnauthorizedClientError(self.client)

        if self.response_type != 'code':
            raise errors.UnsupportedResponseTypeError(self)
