from pauth.requests import AuthorizationRequest, MakeOAuthRequest


def request_authorization(request):
    return MakeOAuthRequest(AuthorizationRequest, request)
