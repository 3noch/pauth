from pauth.requests import authorization
from errors import UnconfiguredError


def _unconfigured():
    """
    Raises an UnconfiguredError whenever its called. Its meant to just
    flag the library-user that something's not configured right.
    """
    raise UnconfiguredError('This middleware configuration hasn\'t been configured yet. '
                            'Did you forget to call `pauth.conf.initialize()`?')


class PauthMiddleware(object):
    def __init__(self):
        self.credentials_readers = {}

    def client_is_registered(self, id):
        _unconfigured()

    def client_is_authorized(self, id, secret):
        _unconfigured()

    def client_has_scope(self, id, scope):
        _unconfigured()

    def adapt_request(self, request):
        _unconfigured()

    def adapt_response(self, response):
        _unconfigured()

    def scope_exists(self, scope):
        _unconfigured()

    def set_credentials_reader(self, method, reader):
        self.credentials_readers[method.lower()] = method

    def get_credentials_reader(self, method):
        return self.credentials_readers.get(method.lower())


# The global middleware object. This is used internally by the library but is configured by the
# library-user. It allows the library-user to hook into the library for his specific use-case or
# framework.
_middleware = None


def initialize(middleware=None):
    """
    Initializes the library. This is the first point-of-entry for the library user. Before the
    library can be used, the library-user must call this function. Calling without arguments will
    initialize the library with the default middleware (mostly unconfigured). Calling with the
    `middleware` argument will initialize the library with a custom subclassed or duck-typed
    middleware.
    """
    if middleware is not None:
        _middleware = PauthMiddleware()
    else:
        _middleware = middleware


def set_default_credentials_readers():
    """
    Sets the default credentials readers to the middleware. This is useful if the library-user
    doesn't want to provide his own credentials readers for common authorization methods like
    Basic and MAC.
    """
    _middleware.set_credentials_reader('Basic', authorization.get_credentials_from_basic)
    _middleware.set_credentials_reader('Mac', authorization.get_credentials_from_mac)
