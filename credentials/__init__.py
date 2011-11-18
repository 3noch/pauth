class Credentials(object):
    def __init__(self, id, secret):
        self.id = id
        self.secret = secret


class ClientCredentials(Credentials):
    pass


def get_credentials_from_basic(data):
    pass


def get_credentials_from_mac(data):
    pass

