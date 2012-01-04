import httplib
from urllib import urlencode

from constants import DEFAULT_CONTENT_TYPE


class Response(object):
    def __init__(self, content, status, headers=None, content_type=DEFAULT_CONTENT_TYPE):
        self.status = status
        self.content = content
        self.headers = headers or {}
        self.content_type = content_type

    def __str__(self):
        return '<{class_name}: {status}>'.format(
            class_name=self.__class__.__name__,
            status=self.status)


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
        return '<{class_name}: {error}>'.format(
            class_name=self.__class__.__name__,
            error=self.id)
