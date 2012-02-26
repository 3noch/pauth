from pauth.errors import PauthError
from pauth.requests import errors, parameters as params
from pauth.requests.authorization import get_credentials_by_method
from pauth.requests.metarequest import BaseRequest


class BaseAuthorizationRequest(BaseRequest):
    ALLOWED_METHOD = 'GET'
    ALLOWED_RESPONSE_TYPE = None

    redirect_uri = params.RedirectUriParameter()
    state = params.StateParameter()
    response_type = params.ResponseTypeParameter(required=True, expected_value=ALLOWED_RESPONSE_TYPE)
    client = params.ClientParameter(required=True)
    scopes = params.ScopeParameter()


class BaseAccessTokenRequest(BaseRequest):
    ALLOWED_METHOD = 'POST'
    ALLOWED_GRANT_TYPE = None

    redirect_uri = params.RedirectUriParameter()
    grant_type = params.GrantTypeParameter(required=True, expected_value=ALLOWED_GRANT_TYPE)
    code = params.CodeParameter(required=True)
