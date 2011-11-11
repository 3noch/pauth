from pauth.conf import config


class Client(object):
    def __init__(self, credentials):
        self.credentials = credentials

    def is_registered(self):
        return config.clients.is_registered(self.id)

    def is_authorized(self):
        return config.clients.is_authorized(self.id, self.secret)
