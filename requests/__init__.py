from abc import ABCMeta, abstractmethod

from pauth.clients import Client
from pauth.conf import config
from pauth.credentials import ClientCredentials


class Request(object):
    __metaclass__ = ABCMeta

    required_parameters = ()

    def __new__(cls, request):
        return config.requests.adapter(request)

    def __init__(self, method='GET', headers=None, parameters=None):
        self.method = method
        self.headers = headers or {}
        self.parameters = parameters or {}

        if 'client_id' in self.parameters:
            credentials = ClientCredentials(self.parameters['client_id'],
                                            self.parameters.get('client_secret'))
            self.client = Client(credentials)
        else:
            self.client = None

        self.response_type = self.parameters.get('response_type')
        self.state = self.parameters.get('state')

    @abstractmethod
    def validate(self):
        pass

    def _has_required_parameters(self):
        return all(p in self.required_parameters for p in self.parameters)
