from pauth.requests import authorization
from pauth.errors import PauthError


class UnconfiguredError(PauthError):
    """
    An error meant to flag the library-user that something is not configured right.
    """
    def __str__(self):
        return ("This Pauth adapter configuration has not been configured yet. "
                'Did you forget to call `pauth.conf.initialize()`?')


class PauthAdapter(object):
    def __init__(self):
        self._credentials_readers = {}

    def adapt_request(self, cls, request):
        raise UnconfiguredError()

    def adapt_response(self, response):
        raise UnconfiguredError()

    def client_is_registered(self, client):
        raise UnconfiguredError()

    def client_is_authorized(self, client, credentials=None):
        raise UnconfiguredError()

    def client_has_scope(self, client, scope):
        raise UnconfiguredError()

    def get_client(self, id):
        return id

    def get_scope(self, id):
        return id

    def scope_exists(self, id):
        return self.get_scope(id) is not None

    def set_credentials_reader(self, method, reader):
        self._credentials_readers[method.lower()] = reader

    def get_credentials_reader(self, method):
        return self._credentials_readers.get(method.lower())


# The global adapter object. This is used internally by the library but is configured by the
# library-user. It allows the library-user to hook into the library for his specific use-case or
# framework.
adapter = None


def initialize(new_adapter=None):
    """
    Initializes the library. This is the first point-of-entry for the library user. Before the
    library can be used, the library-user must call this function. Calling without arguments will
    initialize the library with the default adapter (mostly unconfigured). Calling with the
    `new_adapter` argument will initialize the library with a custom subclassed or duck-typed
    adapter.
    """
    global adapter
    if new_adapter is None:
        adapter = PauthAdapter()
    else:
        adapter = new_adapter


def set_default_credentials_readers():
    """
    Sets the default credentials readers to the adapter. This is useful if the library-user doesn't
    want to provide his own credentials readers for common authorization methods like HTTP Basic.
    """
    adapter.set_credentials_reader('Basic', authorization.get_credentials_from_basic)
