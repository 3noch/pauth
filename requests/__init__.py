from pauth.errors import PauthError
from pauth.requests import errors, parameters as params
from pauth.requests.authorization import get_credentials_by_method
from pauth.requests.metarequest import BaseRequest


def MakeOAuthRequest(cls, request):
    """
    A factory for generating Request objects from a library-user's request. This factory uses the
    global adapter configuration to call a adapter function defined by the library-user that
    converts their own requests into an OAuthRequest that our library will understand.
    """
    from pauth.conf import adapter
    return adapter.adapt_request(cls, request)


class BaseAuthorizationRequest(BaseRequest):
    ALLOWED_METHOD = 'GET'
    ALLOWED_RESPONSE_TYPE = None

    redirect_uri = params.RedirectUriParameter(propagate=True)
    state = params.StateParameter(propagate=True)
    response_type = params.ResponseTypeParameter(required=True, expected_value=ALLOWED_RESPONSE_TYPE)
    client = params.ClientParameter(required=True)
    scope = params.ScopeParameter()


class BaseAccessTokenRequest(BaseRequest):
    ALLOWED_METHOD = 'POST'
    ALLOWED_GRANT_TYPE = None

    redirect_uri = params.RedirectUriParameter(propagate=True)
    grant_type = params.GrantTypeParameter(required=True, expected_value=ALLOWED_GRANT_TYPE)
    code = params.CodeParameter(required=True)
