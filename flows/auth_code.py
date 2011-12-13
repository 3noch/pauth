from pauth.requests import BaseAuthorizationRequest, MakeOAuthRequest


class AuthorizationCodeFlow():
    def request_authorization(request, client, scopes, redirect_uri, state=None):
        pass


class AuthorizationRequest(BaseAuthorizationRequest):
    required_response_type = 'code'


def request_authorization(request):
    return MakeOAuthRequest(AuthorizationRequest, request)
