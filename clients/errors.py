from pauth.errors import OAuthError


class ClientError(OAuthError):
    """
    A base exception class for all OAuth errors having to do with clients.
    """
    id = 'invalid_client'
    description = 'Invalid client: {id}'

    def __init__(self, client):
        self.client = client

    def __repr__(self):
        return self.description.format(
            id=self.client.id if self.client is not None else '[empty]')


class UnknownClientError(ClientError):
    description = 'Unknown client: {id}'


class UnauthorizedClientError(ClientError):
    id = 'unauthorized_client'
    description = 'Unauthorized client: {id}'
