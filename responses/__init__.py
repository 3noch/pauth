from constants import DEFAULT_CONTENT_TYPE, MOVED_PERMANENTLY


class Response(object):
    def __init__(self, status, content, headers=None, content_type=DEFAULT_CONTENT_TYPE):
        self.status = status
        self.content = content
        self.headers = headers or {}
        self.content_type = content_type

    def __repr__(self):
        return '<{class_name}: {status}>'.format(
            class_name=self.__class__.__name__,
            status=self.status)


class ErrorResponse(Response):
    def __init__(self, id, description=None, uri=None):
        self.id = id
        self.description = description
        self.uri = uri
        super(ErrorResponse, self).__init__(MOVED_PERMANENTLY, description)

    def __repr__(self):
        return '<{class_name}: {error}>'.format(
            class_name=self.__class__.__name__,
            error=self.id)
