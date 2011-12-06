from pauth.conf import PauthMiddleware, initialize, set_default_credentials_readers


class MockMiddleware(PauthMiddleware):
    pass


def setup_mock_middleware():
    initialize(MockMiddleware())
    set_default_credentials_readers()
