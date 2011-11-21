class Credentials(object):
    def __init__(self, id, secret):
        self.id = id
        self.secret = secret


class ClientCredentials(Credentials):
    pass
