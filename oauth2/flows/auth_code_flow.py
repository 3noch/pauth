from pauth import errors
from pauth.requests import Request


class AuthorizationRequest(Request):
    required_parameters = ('client_id', 'response_type')

    def validate(self):
        if not all(p in self.required_parameters for p in self.parameters):
            raise errors.InvalidAuthorizationRequestError('Some required request parameters are missing.')


def request_authorization(request):
    auth_request = AuthorizationRequest(request)

    if not auth_request.client.is_registered():
        raise errors.UnknownClientError(auth_request.client)

    if not auth_request.client.is_authorized():
        raise errors.UnauthorizedClientError(auth_request.client)

    return auth_request
