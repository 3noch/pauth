from nose import with_setup
from nose.tools import raises

import authorization
import errors
from pauth.requests import Request
from pauth.test_helpers import MockAdapter, setup_mock_adapter


class MockRequest(Request):
    required_parameters = ('required1', 'required2')


def setup_credentials_reader():
    from pauth.conf import initialize
    mock_adapter = MockAdapter()
    initialize(mock_adapter)
    mock_adapter.set_credentials_reader('test', lambda x: x)


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


def test_request_has_required_parameters():
    # a request without any required parameters always has its required parameters
    assert Request()._has_required_parameters()

    # a request with required parameters
    request = MockRequest()
    assert not request._has_required_parameters()

    request.parameters['not-required'] = 'value1'
    assert not request._has_required_parameters()

    request.parameters['required1'] = 'value1'
    request.parameters['required2'] = 'value2'
    assert request._has_required_parameters()


def test_request_has_header():
    request = Request()
    assert not request.has_header('not-there')

    request.headers['a-header'] = 'header-value'
    assert not request.has_header('not-there')
    assert request.has_header('a-header')
    assert request.has_header('A-Header')


def test_request_get_header():
    request = Request()
    assert request.get_header('not-there') is None

    request.headers['a-header'] = 'header-value'
    assert request.get_header('not-there') is None
    assert request.get_header('a-header') == 'header-value'
    assert request.get_header('A-Header') == 'header-value'


@with_setup(setup_mock_adapter)
def test_request_get_credentials_valid():
    request = Request()
    assert request.get_credentials() is None

    username = 'a-username'
    password = 'top-secret'
    request.headers['Authorization'] = 'Basic ' + '{0}:{1}'.format(username, password).encode('base64')

    credentials = request.get_credentials()
    assert credentials.id == username
    assert credentials.secret == password


@with_setup(setup_mock_adapter)
@raises(errors.UnknownAuthenticationMethod)
def test_request_get_credentials_invalid():
    request = Request()
    request.headers['Authorization'] = 'Invalid no-data'
    request.get_credentials()
