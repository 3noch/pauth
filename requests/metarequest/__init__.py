from pauth.errors import PauthError
from pauth.requests.errors import MissingQueryArgumentsError
from pauth.requests.parameters import RequestParameter
from pauth.requests.metarequest.dict_utils import copy_dict_except, dicts_intersect


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

        # Get the OAuth parameters from the new class and all its parents.
        oauth_attrs = get_oauth_attrs_from_bases(bases)
        oauth_attrs.update(get_oauth_attrs(attrs)) # These OAuth parameters always trump those from the bases

        new_attrs = copy_dict_except(attrs, oauth_attrs.iterkeys())
        new_attrs['_OAUTH_ATTRS'] = oauth_attrs
        new_attrs['_parse_query_args'] = create_parse_query_args(oauth_attrs)
        new_attrs['_propagate'] = create_propagate(oauth_attrs)
        new_attrs['_meta_init'] = create_meta_init(oauth_attrs)

        return super(RequestMetaclass, mcs).__new__(mcs, name, bases, new_attrs)


def get_oauth_attrs_from_bases(bases):
    """
    Forms a compiled dictionary of all OAuth attributes from a list of base classes.
    The process also raises an error if any of the base classes define the same
    OAuth parameter.
    """
    oauth_attrs = {}

    for base in bases:
        if hasattr(base, '_OAUTH_ATTRS'):
            if dicts_intersect(base._OAUTH_ATTRS, oauth_attrs):
                raise MultipleOAuthParamDefinitionsInParents()
            else:
                oauth_attrs.update(base._OAUTH_ATTRS)

    return oauth_attrs


def create_meta_init(oauth_attrs):
    """
    Creates a `_meta_init` method which simply initializes all of the OAuth parameters as
    instance variables with default values.
    """
    def _meta_init(self):
        for name, param in oauth_attrs.iteritems():
            setattr(self, name, None)

    return _meta_init


def create_parse_query_args(oauth_attrs):
    """
    Creates a `_parse_query_args()` method which parses a request's query arguments for its
    expected OAuth parameters.
    """
    def _parse_query_args(self):
        """
        Parses each query argument based on the request's OAuth parameters. The parameters
        are parsed in order of their priority.
        """
        sorted_keys = sorted(oauth_attrs, key=lambda key: oauth_attrs[key].PRIORITY)

        for key in sorted_keys:
            setattr(self, key, oauth_attrs[key].get_from_request(self))

    return _parse_query_args


def create_propagate(oauth_attrs):
    """
    Creates a `_propagate()` method which is used to copy certain, important class members to
    other objects (like errors, for example).
    """
    propagated_attrs = {key: param for key, param in oauth_attrs.iteritems()
                        if param.propagate}

    def _propagate(self, recipient):
        for name, param in propagated_attrs.iteritems():
            setattr(recipient, name, getattr(self, name))

    return _propagate


def get_oauth_attrs(attrs):
    """
    Takes a dictionary of class attributes and returns only the attributes that define OAuth
    parameters. See `is_oauth_attr()` for a description of attributes that define OAuth
    parameters.
    """
    return {key: value for key, value in attrs.iteritems()
            if is_oauth_attr(key, value)}


def is_oauth_attr(attr_name, attr_value):
    """
    Returns `True` for an attribute that defines a request's OAuth parameter.

    An OAuth parameter is distinguished by the following criteria:
        * Attribute's name does not start with any `_` characters
        * Attribute's name is all lower-case.
        * Attribute's value is an instance of the `RequestParameter` class
    """
    return (not attr_name.startswith('_')
            and attr_name.lower() == attr_name
            and isinstance(attr_value, RequestParameter))


class BaseRequest(object):
    __metaclass__ = RequestMetaclass

    _OAUTH_ATTRS = {}

    ALLOWED_METHOD = 'GET'

    def __init__(self, method=ALLOWED_METHOD, headers=None, query_args=None):
        """
        This constructor defines our internally-standard interface for creating a request.
        """
        self.method = method
        self.headers = headers or {}
        self.query_args = query_args or {}

        self._meta_init()
        self._parse_query_args()

    def _meta_init(self):
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
