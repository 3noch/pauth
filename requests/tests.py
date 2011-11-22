import authorization
from errors import UnknownAuthenticationMethod
from pauth import conf


class MockMiddleware(conf.PauthMiddleware):
	pass


def mock_credentials_reader(data):
	return data


def setup_test_credentials_reader():
	mockMiddleware = MockMiddleware()
	conf.initialize(mockMiddleware)
	mockMiddleware.set_credentials_reader('test', mock_credentials_reader)


@with_setup(setup_test_credentials_reader)
def test_get_credentials_by_method_with_test_reader():
	assert authorization.get_credentials_by_method('test', True)

	try:
		authorization.get_credentials_by_method('not-there', [])
	except UnknownAuthenticationMethod:
		pass


def test_get_credentials_from_basic():
	pass


def test_get_credentials_from_mac():
    pass
