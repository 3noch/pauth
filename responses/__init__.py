class Response(object):
    def __init__(self, status, content, content_type=None):
        self.status = status
        self.content = content
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
        super(ErrorResponse, self).__init__(301, description)

    def __repr__(self):
        return '<{class_name}: {error}>'.format(
            class_name=self.__class__.__name__,
            error=self.id)
