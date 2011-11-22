from nose import with_setup

import authorization
from errors import UnknownAuthenticationMethod
from pauth.test_helpers import MockMiddleware


def mock_credentials_reader(data):
    return data


def setup_credentials_reader():
    from pauth.conf import initialize
    mock_middleware = MockMiddleware()
    initialize(mock_middleware)
    mock_middleware.set_credentials_reader('test', mock_credentials_reader)


@with_setup(setup_credentials_reader)
def test_get_credentials_by_method():
    assert authorization.get_credentials_by_method('test', True)

    try:
        authorization.get_credentials_by_method('not-there', [])
    except UnknownAuthenticationMethod:
        pass


def test_get_credentials_from_basic():
    pass


def test_get_credentials_from_mac():
    pass
