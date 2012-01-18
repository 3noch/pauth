from pauth.requests import BaseAuthorizationRequest, MakeOAuthRequest


class AuthorizationRequest(BaseAuthorizationRequest):
    ALLOWED_RESPONSE_TYPE = 'code'


def request_authorization(request):
    return MakeOAuthRequest(AuthorizationRequest, request)
