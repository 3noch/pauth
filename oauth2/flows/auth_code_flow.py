from poth.hooks import clients, requests


class Credentials(object):
    def __init__(self, id, secret):
        self.id = id
        self.secret = secret


class ClientCredentials(Credentials):
    pass


class OAuthClient(object):
    def __init__(self, credentials):
        self.credentials = credentials

    def is_registered(self):
        return clients.is_registered(self.id)
    
    def is_authorized(self):
        return clients.is_authorized(self.id, self.secret)


class OAuthError(Exception):
    pass


class RequestError(OAuthError):
    pass


class InvalidAuthorizationRequestError(RequestError):
    pass


class UnknownClientError(RequestError):
    pass


class UnauthorizedClientError(RequestError):
    pass


class OAuthRequest(object):
    def __new__(cls, request):
        return requests.adapter(request)

    def __init__(self, method='GET', headers=None, parameters=None):
        self.method = method
        self.headers = headers or {}
        self.parameters = parameters or {}

        if 'client_id' in self.parameters:
            credentials = ClientCredentials(self.parameters['client_id'],
                                            self.parameters.get('client_secret'))
            self.client = OAuthClient(credentials)
        else:
            self.client = None
        
        self.response_type = self.parameters.get('response_type')
        self.state = self.parameters.get('state')

    def validate(self):
        pass


class AuthorizationRequest(OAuthRequest):
    required_parameters = ('client_id', 'response_type')

    def validate(self):
        if not all(p in self.required_parameters for p in self.parameters)
            raise InvalidAuthorizationRequestError('Some required request parameters are missing.')
        


def request_authorization(request):
    auth_request = AuthorizationRequest(request)
    
    if not auth_request.client.is_registered():
        raise UnknownClientError(oauth_request.client)

    if not auth_request.client.is_authorized():
        raise UnauthorizedClientError(client)
    
    return oauth_request
    
