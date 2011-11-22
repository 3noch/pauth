from nose import with_setup
from nose.tools import raises

import authorization
import errors
from pauth.test_helpers import MockMiddleware


def setup_credentials_reader():
    from pauth.conf import initialize
    mock_middleware = MockMiddleware()
    initialize(mock_middleware)
    mock_middleware.set_credentials_reader('test', lambda x: x)


@with_setup(setup_credentials_reader)
def test_get_credentials_by_method_valid():
    assert authorization.get_credentials_by_method('test', True)


@with_setup(setup_credentials_reader)
@raises(errors.UnknownAuthenticationMethod)
def test_get_credentials_by_method_invalid():
    authorization.get_credentials_by_method('not-there', [])


def test_get_credentials_from_basic_valid():
    username = 'test-username'
    password = 'test-password'
    signature = '{0}:{1}'.format(username, password)
    encoded_signature = signature.encode('base64')
    credentials = authorization.get_credentials_from_basic(encoded_signature)

    assert credentials.id == username
    assert credentials.secret == password


@raises(errors.MalformedAuthenticationCredentials)
def test_get_credentials_from_basic_invalid():
        authorization.get_credentials_from_basic('')


def test_get_credentials_from_mac():
    pass
