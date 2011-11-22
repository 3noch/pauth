class Client(object):
    def __init__(self, credentials):
        self.credentials = credentials

    def is_registered(self):
        from pauth.conf import middleware
        return middleware.client_is_registered(self.id)

    def is_authorized(self):
        from pauth.conf import middleware
        return middleware.client_is_authorized(self.id, self.secret)
