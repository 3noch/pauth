from authorization import get_credentials_by_method
import errors
import extractors
import validators


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
    VALIDATORS = (validators.has_method(('GET')))
    EXTRACTORS = ()

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

    def _validate(self):
        """
        Raises an error for anything about the request that isn't valid.
        """
        for validator in self.VALIDATORS:
            validator(self)

    def _extract(self):
        """
        Extracts all of the necessary information from the request and
        raises errors if problems occur.
        """
        for extractor in self.EXTRACTORS:
            extractor(self)

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

    def _propagate_error(self, error):
        """
        Allows the request class to attach pertinent information to an error before it
        gets raised. This isn't just convenient but essential when the error needs to be
        sent to the requester via the redirect URI that was provided in the request. This
        method takes an error and returns a modified version of the error.
        """
        error.state = self.state
        return error


class RequestWithRedirectUri(Request):
    def __init__(self, method='GET', headers=None, parameters=None):
        super(RequestWithRedirectUri, self).__init__(method, headers, parameters)
        self.redirect_uri = None
        self._extract_redirect_uri()

    def _propagate_error(self, error):
        error = super(BaseAuthorizationRequest, self)._propagate_error(error)
        error.redirect_uri = self.redirect_uri
        return error


class BaseAuthorizationRequest(RequestWithRedirectUri):
    VALIDATORS = (validators.has_method(('GET')),
                  validators.has_parameters(('client_id', 'response_type')))
    EXTRACTORS = (extractors.extract_response_type,
                  extractors.extract_client,
                  extractors.extract_scopes)
    def __init__(self, method='GET', headers=None, parameters=None):
        super(BaseAuthorizationRequest, self).__init__(method, headers, parameters)
        self.response_type = None
        self.client = None
        self.credentials = None
        self.scopes = []

        self._validate()
        self._extract()


class BaseAccessTokenRequest(RequestWithRedirectUri):
    VALIDATORS = (validators.has_method(('POST')),
                  validators.has_parameters(('grant_type', 'code', 'redirect_uri')))
    EXTRACTORS = (extractors.extract_grant_type)

    def __init__(self, method='GET', headers=None, parameters=None):
        super(BaseAccessTokenRequest, self).__init__(method, headers, parameters)
        self.response_type = None
        self.code = None

        self._validate()
        self._extract()
