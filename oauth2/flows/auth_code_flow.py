from pauth.errors import OAuthError
from pauth.requests import AuthorizationRequest


def request_authorization(request):
    try:
        auth_request = AuthorizationRequest(request)
    except OAuthError as e:
        return e.response

    return auth_request
