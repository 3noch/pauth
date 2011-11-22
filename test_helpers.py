from pauth.conf import PauthMiddleware, initialize


class MockMiddleware(PauthMiddleware):
    pass


def setup_mock_middleware():
    initialize(MockMiddleware())
