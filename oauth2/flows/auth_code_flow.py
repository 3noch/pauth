from pauth.errors import OAuthError
from pauth.requests import Request
from pauth.requests import errors as request_errors


class AuthorizationRequest(Request):
    required_parameters = ('client_id', 'response_type')

    def validate(self):
        super(AuthorizationRequest, self).validate()

        if self.response_type != 'code':
            raise request_errors.UnsupportedResponseTypeError(self)


def request_authorization(request):
    try:
        auth_request = AuthorizationRequest(request)
    except OAuthError as e:
        return e.response


