from httplib import OK
from httplib2 import Http, HttpLib2Error
from simplejson import loads, JSONDecodeError

from django.conf import settings


def get_scopes(client_id=None):
    http = Http()
    uri = 'http://{authorize_host}/scopes/{client_id}'.format(
        authorize_host=settings.AUTHORIZATION_HOST,
        client_id=client_id or '')
    try:
        response, content = http.request(uri)
        if response.status == OK:
            return loads(content)
    except (HttpLib2Error, JSONDecodeError):
        pass
    return None
