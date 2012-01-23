import json


class AccessToken(object):
    def __init__(self, fields=None):
        self.fields = fields or {}

    def to_json(self):
        return json.dumps(self.fields)


class BearerAccessToken(AccessToken):
    pass


class MacAccessToken(AccessToken):
    pass
