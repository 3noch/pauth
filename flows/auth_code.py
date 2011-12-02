from pauth.requests import BaseAuthorizationRequest, MakeOAuthRequest


class AuthorizationRequest(BaseAuthorizationRequest):
    required_response_type = 'code'


def request_authorization(request):
    return MakeOAuthRequest(AuthorizationRequest, request)
