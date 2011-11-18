from errors import UnconfiguredError


def _unconfigured():
    """
    Raises an UnconfiguredError whenever its called. Its meant to just
    flag the library-user that something's not configured right.
    """
    raise UnconfiguredError()


class Configuration(object):
    """
    A base configuration class. It doesn't do anything yet. So far it
    just serves to provide hierarchy.
    """
    pass


class PauthConfiguration(Configuration):
    """
    The base Pauth configuration class. There should only be one of
    these! Why not use the Singleton pattern? Because Python doesn't
    have very good ways to implement that. Just don't break the rules.
    """
    def __init__(self):
        self.clients = ClientConfiguration()
        self.requests = RequestConfiguration()
        self.responses = ResponseConfiguration()
        self.scopes = ScopeConfiguration()


class ClientConfiguration(Configuration):
    """
    Configuration class for clients. The only instance of this should
    be in a member variable of PauthConfiguration.
    """
    def __init__(self):
        self.is_registered = _unconfigured
        self.is_authorized = _unconfigured


class RequestConfiguration(Configuration):
    """
    Configuration class for requests. The only instance of this should
    be in a member variable of PauthConfiguration.
    """
    def __init__(self):
        self.adapter = _unconfigured
        self.credentials_readers = {}


class ResponseConfiguration(Configuration):
    """
    Configuration class for responses. The only instance of this should
    be in a member variable of PauthConfiguration.
    """
    def __init__(self):
        self.adapter = _unconfigured


class ScopeConfiguration(Configuration):
    """
    Configuration class for scopes. The only instance of this should
    be in a member variable of PauthConfiguration.
    """
    def __init__(self):
        self.is_scope = _unconfigured
        self.has_scope = _unconfigured


# `config` is the global configuration class. It's meant to be
# used by the library-user to hook into his own setup.
config = PauthConfiguration()


# These are decorators to make defining the configuration hooks
# really simple.
def defines_client_is_registered(f):
    config.clients.is_registered = f
    return f


def defines_client_is_authorized(f):
    config.clients.is_authorized = f
    return f


def defines_request_adapter(f):
    config.requests.adapter = f
    return f


def defines_response_adapter(f):
    config.responses.adapter = f
    return f

