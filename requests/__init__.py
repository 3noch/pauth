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
    def __new__(cls, name, bases, attrs):
        oauth_attrs = cls.get_oauth_attrs(attrs)

        new_attrs = copy_dict_except(attrs, oauth_attrs.key())
        new_attrs['_validate_parameters'] = cls.create_validate_parameters(oauth_attrs)
        new_attrs['_parse_query_args'] = cls.create_parse_query_args(oauth_attrs)
        new_attrs['_propagate'] = cls.create_propagate(oauth_attrs)

        return super(RequestMetaclass, cls).__new__(name, bases, new_attributes)

    @classmethod
    def create_validate_query_args(cls, oauth_attrs):
        required_params = [param for key, param in attrs.iteritems()
                           if param.required]
        required_param_names = [param.name for param in cls.get_required_params(oauth_attrs)]

        def _validate_query_args(self):
            missing_args = [arg for arg in self.query_args
                            if arg not in required_param_names]

            if missing_args:
                raise errors.MissingQueryArgumentsError(self, missing_args)

        return _validate_parameters

    @classmethod
    def create_parse_query_args(cls, oauth_attrs):
        def _parse_query_args(self):
            for name, param in oauth_attrs.iteritems():
                setattr(self, name, param.get_from_request(self))

        return _parse_query_args

    @classmethod
    def create_propagate(cls, oauth_attrs):
        propagated_attrs = {key: param for key, param in oauth_attrs.iteritems()
                            if param.propagate}

        def _propagate(self, recipient):
            for name, param in propagated_attrs.iteritems():
                setattr(recipient, name, getattr(self, name))

        return _propagate

    @classmethod
    def get_oauth_attrs(cls, attributes):
        return {key: value for key, value in attrs.iteritems()
                if cls.is_oauth_attr(key)]

    @classmethod
    def is_oauth_attrs(cls, attr_name):
        """
        Returns `True` for an attribute that defines a request's OAuth
        parameter. Expected parameters are lower-case and don't
        start with `__`.
        """
        return (not attr_name.startswith('__')
                and attr_name.lower() == attr_name)


class Request(object):
    __metaclass__ = RequestMetaclass

    ALLOWED_METHOD = 'GET'

    def __init__(self, method=ALLOWED_METHOD, headers=None, query_args=None):
        """
        This constructor defines our internally-standard interface for creating a
        request.
        """
        self.method = method
        self.headers = headers or {}
        self.query_args = query_args or {}

        self._validate()

    def _validate():
        """
        Validates the request for cursory problems such as missing parameters and
        invalid methods.
        """
        pass

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
    ALLOWED_METHOD = 'GET'
    ALLOWED_RESPONSE_TYPE = None

    redirect_uri = params.RedirectUriParameter(propagate=True)
    state = params.StateParameter(propagate=True)
    response_type = params.ResponseTypeParameter(required=True, expected_value=ALLOWED_RESPONSE_TYPE)
    client = params.ClientParameter(required=True)
    scope = params.ScopeParameter()


class BaseAccessTokenRequest(Request):
    ALLOWED_METHOD = 'POST'
    ALLOWED_GRANT_TYPE = None

    redirect_uri = params.RedirectUriParameter(propagate=True)
    grant_type = params.GrantTypeParameter(required=True, expected_value=ALLOWED_GRANT_TYPE)
    code = params.CodeParameter(required=True)
