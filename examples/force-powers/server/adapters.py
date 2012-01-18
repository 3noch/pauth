import sys
sys.path.append('../../../..')


from pauth import conf


class Adapter(conf.PauthAdapter):
    def adapt_request(self, cls, request):
        return cls(request.method,
                   self.get_standard_headers(request.META),
                   dict(request.GET.items()
                        if request.method == 'GET'
                        else request.POST.items()))

    def adapt_response(self, response):
        from django.http import HttpResponse
        new_response = HttpResponse(content=response.content,
                                    status=response.status,
                                    content_type=response.content_type)

        for header, value in response.headers.items():
            new_response[header] = value

        return new_response

    def client_is_authorized(self, client, credentials=None):
        return False if credentials is None else client.secret == credentials.secret

    def client_is_registered(self, client):
        return True

    def client_has_scope(self, client, scope):
        return scope in client.allowed_scopes.all()

    def get_client(self, id):
        from clients.models import Client
        try:
            return Client.objects.get(id=id)
        except Client.DoesNotExist:
            return None

    def get_scope(self, scope):
        from scopes.models import Scope
        try:
            return Scope.objects.get(id=scope)
        except Scope.DoesNotExist:
            return None

    def get_standard_headers(self, meta):
        exceptions = ('CONTENT_LENGTH', 'CONTENT_TYPE')
        prefix = 'HTTP_'

        headers = {}
        for field, value in meta.items():
            header = None
            if field.startswith(prefix):
                header = field[len(prefix):]
            elif field in exceptions:
                header = field

            if header is not None:
                header = field.replace('_', '-')
                headers[header] = value

        return headers


conf.initialize(Adapter())
conf.set_default_credentials_readers()
