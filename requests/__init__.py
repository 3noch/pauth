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


def copy_dict_except(source, except_keys):
    """
    Copies a dictionary into a new dictionary, but leaves out any keys in
    the `except_keys` list.
    """
    new_dict = {}
    for key, value in source.iteritems():
        if key not in except_keys:
            new_dict[key] = value

    return new_dict


class RequestMetaclass(type):
    def __new__(cls, name, bases, attributes):
        expected_parameters = cls.get_expected_parameters(attributes)
        new_init = cls.create_new_init(parameters=expected_parameters,
                                       old_init=attributes.get('__init__'))

        new_attributes = copy_dict_except(attributes, expected_parameters)
        new_attributes['__init__'] = new_init

        return super(RequestMetaclass, cls).__new__(name, bases, new_attributes)

    @classmethod
    def create_new_init(cls, parameters, old_init=None):
        def __init__(self, method='GET', headers=None, parameters=None):
            super(self.__class__, self).__init__(method, headers, parameters)

            for parameter in parameters:
                setattr(self, parameter, None)

            if old_init is not None:
                old_init(self)

        return __init__

    @classmethod
    def get_expected_parameters(cls, attributes):
        return [key for key in attributes.iterkeys()
                if cls.is_expected_parameter(key)]

    @classmethod
    def is_expected_parameter(cls, parameter_name):
        """
        Returns `True` for a class attribute that defines an expected
        parameter of a request. Expected parameters are lower-case and don't
        start with `__`.
        """
        return (not parameter_name.startswith('__')
                and parameter_name.lower() == parameter_name)


class Request(object):
    def __init__(self, method='GET', headers=None, parameters=None):
        """
        This constructor defines our internally-standard interface for creating a
        request.
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
    response_type = params.ResponseTypeParameter(required=True, expected_value=ALLOWED_RESPONSE_TYPE)
    client = params.ClientParameter(required=True)
    scope = params.ScopeParameter()


class BaseAccessTokenRequest(Request):
    __metaclass__ = RequestMetaclass

    ALLOWED_METHOD = 'POST'
    ALLOWED_GRANT_TYPE = None

    redirect_uri = params.RedirectUriParameter(propagate=True)
    grant_type = params.GrantTypeParameter(required=True, expected_value=ALLOWED_GRANT_TYPE)
    code = params.CodeParameter(required=True)
