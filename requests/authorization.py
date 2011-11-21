from errors import UnknownAuthenticationMethod
from pauth.conf import _middleware


def get_credentials_by_method(method, data):
    reader = _middleware.get_credentials_reader(method)
    if reader is None:
        raise UnknownAuthenticationMethod(method)
    else:
        return reader(data)


def get_credentials_from_basic(data):
    pass


def get_credentials_from_mac(data):
    pass
