import httplib
from urllib import urlencode

from constants import DEFAULT_CONTENT_TYPE


class Response(object):
    def __init__(self, content, status, headers=None, content_type=DEFAULT_CONTENT_TYPE):
        self.status = status
        self.content = content
        self.headers = headers or {}

        headers['Content-Type': content_type]

    def __repr__(self):
        return '<{class_name}: {status}>'.format(
            class_name=self.__class__.__name__,
            status=self.status)


class AccessTokenResponse(Response):
    CONTENT_TYPE = 'application/json;charset=utf-8'
    HEADERS = {'Cache-Control': 'no-store',
               'Pragma:' 'no-cache'}

    def __init__(self, access_token=None):
        super(AccessTokenResponse, self).__init__(
            content=access_token.to_json(),
            headers=self.HEADERS,
            content_type=self.CONTENT_TYPE)
        self.access_token = access_token

    def __repr__(self):
        return '<{class_name}: {access_token}>'.format(
            class_name=self.__class__.__name__,
            content=self.access_token)



class ErrorResponse(Response):
    def __init__(self, id, description=None, uri=None, state=None, redirect_uri=None):
        redirect_header = None
        parameters = {'error': id,
                      'error_description': description,
                      'error_uri': uri,
                      'state': state}

        if redirect_uri is not None:
            full_uri = '{redirect_uri}?{parameters}'.format(
                redirect_uri=redirect_uri.rstrip('? '),
                parameters=urlencode({k: v for k, v in parameters.items()
                                      if v is not None}))
            redirect_header = {'Location': full_uri}

        super(ErrorResponse, self).__init__(content=description,
                                            status=httplib.MOVED_PERMANENTLY,
                                            headers=redirect_header)

        self.id = id
        self.description = description
        self.uri = uri
        self.state = state
        self.redirect_uri = redirect_uri

    def __str__(self):
        return 'OAuth Error: {id} "{description}"'.format(
            id=self.id
            description=self.description)

    def __repr__(self):
        return '<{class_name}: {error}>'.format(
            class_name=self.__class__.__name__,
            error=self.id)
