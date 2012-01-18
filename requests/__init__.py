from authorization import get_credentials_by_method
from pauth.errors import PauthError
import errors
import parameters as params


def MakeOAuthRequest(cls, request):
    """
    A factory for generating Request objects from a library-user's request. This factory uses the
    global adapter configuration to call a adapter function defined by the library-user that
    converts their own requests into an OAuthRequest that our library will understand.
    """
    from pauth.conf import adapter
    return adapter.adapt_request(cls, request)


def copy_dict_except(source, except_keys):
    """
    Copies a dictionary into a new dictionary, but leaves out any keys in the `except_keys` list.
    """
    new_dict = {}
    for key, value in source.iteritems():
        if key not in except_keys:
            new_dict[key] = value

    return new_dict


class MethodMustBeOverriddenByMetaclassError(PauthError):
    """
    A trivial error class for exposing the rare case when a class expects one or more of its methods
    to be overridden by its metaclass constructor, but they aren't.
    """
    def __str__(self):
        return 'This method must be overridden by a metaclass!'


class RequestMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        """
        Constructs a modified instance of a request class. Here's how it works:

        Any class attributes that are deemed to be OAuth parameters (see `is_oauth_attr()`) are
        taken out of the resulting class and used to create a few helper methods that are attached
        to the resulting class. Those helper methods are:
            * _validate_query_args
            * _parse_query_args
            * _propagate

        The resulting class can use these helper methods to do customized operations on its expected
        OAuth parameters.
        """
        oauth_attrs = mcs.get_oauth_attrs(attrs)

        new_attrs = copy_dict_except(attrs, oauth_attrs.iterkeys())
        new_attrs['_validate_query_args'] = mcs.create_validate_query_args(oauth_attrs)
        new_attrs['_parse_query_args'] = mcs.create_parse_query_args(oauth_attrs)
        new_attrs['_propagate'] = mcs.create_propagate(oauth_attrs)
        new_attrs['OAUTH_PARAMS'] = oauth_attrs.keys()

        return super(RequestMetaclass, mcs).__new__(mcs, name, bases, new_attrs)

    @classmethod
    def create_validate_query_args(cls, oauth_attrs):
        """
        Creates a `_validate_query_args()` method, which does a cursory check of a request's query
        arguments for missing or invalid OAuth parameters.
        """
        required_param_names = [param.NAME for key, param in oauth_attrs.iteritems()
                                if param.required]

        def _validate_query_args(self):
            missing_args = [arg for arg in self.query_args
                            if arg not in required_param_names]

            if missing_args:
                raise errors.MissingQueryArgumentsError(self, missing_args)

        return _validate_query_args

    @classmethod
    def create_parse_query_args(cls, oauth_attrs):
        """
        Creates a `_parse_query_args()` method, which parses a request's query arguments for its
        expected OAuth parameters.
        """
        def _parse_query_args(self):
            for name, param in oauth_attrs.iteritems():
                setattr(self, name, param.get_from_request(self))

        return _parse_query_args

    @classmethod
    def create_propagate(cls, oauth_attrs):
        """
        Creates a `_propagate()` method, which is used to copy certain, important class members to
        other objects (like errors, for example).
        """
        propagated_attrs = {key: param for key, param in oauth_attrs.iteritems()
                            if param.propagate}

        def _propagate(self, recipient):
            for name, param in propagated_attrs.iteritems():
                setattr(recipient, name, getattr(self, name))

        return _propagate

    @classmethod
    def get_oauth_attrs(cls, attrs):
        """
        Takes a dictionary of class attributes and returns only the attributes that define OAuth
        parameters. See `is_oauth_attr()` for a description of attributes that define OAuth
        parameters.
        """
        return {key: value for key, value in attrs.iteritems()
                if cls.is_oauth_attr(key, value)}

    @classmethod
    def is_oauth_attr(cls, attr_name, attr_value):
        """
        Returns `True` for an attribute that defines a request's OAuth parameter.
        An OAuth parameter is distinguished by the following criteria:
            * Attribute's name does not start with any `_` characters
            * Attribute's name is all lower-case.
            * Attribute's value is an instance of the `RequestParameter` class
        """
        return (not attr_name.startswith('_')
                and attr_name.lower() == attr_name
                and isinstance(attr_value, params.RequestParameter))


class Request(object):
    __metaclass__ = RequestMetaclass

    OAUTH_PARAMS = []
    ALLOWED_METHOD = 'GET'

    def __init__(self, method=ALLOWED_METHOD, headers=None, query_args=None):
        """
        This constructor defines our internally-standard interface for creating a request.
        """
        self.method = method
        self.headers = headers or {}
        self.query_args = query_args or {}

        for param in self.OAUTH_PARAMS:
            setattr(self, param, None)

        self._validate_query_args()
        self._parse_query_args()

    def _validate_query_args(self):
        raise MethodMustBeOverriddenByMetaclassError()

    def _parse_query_args(self):
        raise MethodMustBeOverriddenByMetaclassError()

    def _propagate(self, recipient):
        raise MethodMustBeOverriddenByMetaclassError()

    def has_header(self, header):
        """
        Returns `True` when `header` matches at least one of the requests headers without comparing
        case.
        """
        return any(header.lower() == h.lower() for h in self.headers)

    def get_header(self, header):
        """
        Returns the value of the request header that matches `header` (without comparing case) or
        `None` if there is no matching header.
        """
        return next((v for k, v in self.headers.items()
                     if k.lower() == header.lower()), None)

    def get_credentials(self):
        """
        Returns Credentials object created from the information provided in the HTTP `Authorization`
        header, or `None` if this information is absent or unrecognized.
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
            # Intercept any errors raised when getting credentials and attach state and redirection
            # info for this request so that the error will generate the correct response.
            raise self._propagate(error)

    def propagate(self, recipient):
        """
        Allows the request class to attach pertinent information to an error before it gets raised.
        This isn't just convenient but essential when the error needs to be sent to the requester
        via the redirect URI that was provided in the request. This method takes an error and
        returns a modified version of the error.
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
