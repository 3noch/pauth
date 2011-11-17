from errors import UnconfiguredError


def _unconfigured():
    raise UnconfiguredError()


class Configuration(object):
    pass


class PauthConfiguration(Configuration):
    def __init__(self):
        self.clients = ClientConfiguration()
        self.requests = RequestConfiguration()
        self.responses = ResponseConfiguration()
        self.scopes = ScopeConfiguration()


class ClientConfiguration(Configuration):
    def __init__(self):
        self.is_registered = _unconfigured
        self.is_authorized = _unconfigured


class RequestConfiguration(Configuration):
    def __init__(self):
        self.adapter = _unconfigured


class ResponseConfiguration(Configuration):
    def __init__(self):
        self.adapter = _unconfigured


class ScopeConfiguration(Configuration):
    def __init__(self):
        self.is_scope = _unconfigured
        self.has_scope = _unconfigured

# `config` is the global configuration class. It's meant to be
# used by the library's user to hook into his own setup.
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
