from errors import UnconfiguredError


def _unconfigured():
    raise UnconfiguredError()


class Configuration(object):
    pass


class PauthConfiguration(Configuration):
    def __init__(self):
        self.clients = ClientConfiguration()
        self.requests = RequestConfiguration()


class ClientConfiguration(Configuration):
    def __init__(self):
        self.is_registered = _unconfigured
        self.is_authorized = _unconfigured


class RequestConfiguration(Configuration):
    def __init__(self):
        self.adapter = _unconfigured


config = PauthConfiguration()
