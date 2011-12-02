from pauth.requests import BaseAuthorizationRequest, MakeOAuthRequest


class AuthorizationRequest(BaseAuthorizationRequest):
    required_response_type = 'token'


def request_authorization(request):
    return MakeOAuthRequest(AuthorizationRequest, request)
