from pauth.clients import errors as client_errors
from pauth.errors import OAuthError
from pauth.requests import Request
from pauth.requests import errors as request_errors


class AuthorizationRequest(Request):
    required_parameters = ('client_id', 'response_type')

    def validate(self):
        if not self._has_required_parameters():
            raise request_errors.InvalidAuthorizationRequestError('Some required request parameters are missing.')

        if not self.client.is_registered():
            raise client_errors.UnknownClientError(self.client)

        if not self.client.is_authorized():
            raise client_errors.UnauthorizedClientError(self.client)

        if self.response_type != 'code':
            raise request_errors.UnsupportedResponseTypeError(self)


def request_authorization(request):
    try:
        return AuthorizationRequest(request)
    except OAuthError as e:
        return e.response
