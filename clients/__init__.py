from pauth.conf import _middleware


class Client(object):
    def __init__(self, credentials):
        self.credentials = credentials

    def is_registered(self):
        return _middleware.client_is_registered(self.id)

    def is_authorized(self):
        return _middleware.client_is_authorized(self.id, self.secret)
