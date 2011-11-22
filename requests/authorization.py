from errors import UnknownAuthenticationMethod


def get_credentials_by_method(method, data):
    from pauth.conf import middleware
    reader = middleware.get_credentials_reader(method)
    if reader is None:
        raise UnknownAuthenticationMethod(method)
    else:
        return reader(data)


def get_credentials_from_basic(data):
    pass


def get_credentials_from_mac(data):
    pass
