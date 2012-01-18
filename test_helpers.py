import conf


class MockAdapter(conf.PauthAdapter):
    pass


def setup_mock_adapter():
    conf.initialize(MockAdapter())
    conf.set_default_credentials_readers()
