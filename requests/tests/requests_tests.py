from nose import with_setup
from nose.tools import raises

from pauth.requests import errors, Request


class MockRequest(Request):
    required_parameters = ('required1', 'required2')


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
