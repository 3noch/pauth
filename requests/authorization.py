from pauth.credentials import Credentials
import errors


def get_credentials_by_method(method, data):
    from pauth.conf import middleware
    reader = middleware.get_credentials_reader(method)
    if reader is None:
        raise errors.UnknownAuthenticationMethod(method)
    else:
        return reader(data)


def get_credentials_from_basic(data):
    decoded_data = data.decode('base64')
    try:
        username, password = decoded_data.split(':', 1)
    except ValueError:
        raise errors.MalformedAuthenticationCredentials(data)

    return Credentials(username, password)


def get_credentials_from_mac(data):
    pass
