from pauth.clients import errors as client_errors
from pauth.requests import Request
from pauth.requests import errors as request_errors


class AuthorizationRequest(Request):
    required_parameters = ('client_id', 'response_type')

    def validate(self):
        if not self._has_required_parameters():
            raise request_errors.InvalidAuthorizationRequestError('Some required request parameters are missing.')


def request_authorization(request):
    auth_request = AuthorizationRequest(request)

    if not auth_request.client.is_registered():
        raise client_errors.UnknownClientError(auth_request.client)

    if not auth_request.client.is_authorized():
        raise client_errors.UnauthorizedClientError(auth_request.client)

    if auth_request.response_type != 'code':
        raise request_errors.UnsupportedResponseTypeError(auth_request)

    return auth_request
