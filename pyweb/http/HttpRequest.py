from wsgiref.util import guess_scheme, request_uri
from urllib.parse import parse_qs


class HTTPRequest:
    def __init__(self, environ):
        self._env = environ
        self._gateway_interface = environ.get('GATEWAY_INTERFACE')
        self._content_length = environ.get('CONTENT_LENGTH')
        self._message = environ.get('wsgi.input')
        self.schema = guess_scheme(environ)
        self.port = environ.get('SERVER_PORT')
        self.request_method = environ.get('REQUEST_METHOD')
        self.host = environ.get('HTTP_HOST')
        self.path = environ.get('PATH_INFO')
        self.query_string = parse_qs(environ.get('QUERY_STRING'))
        self.full_path = request_uri(environ)
        self.user_agent = environ.get('HTTP_USER_AGENT')
        self.accepted_languages = environ.get('HTTP_ACCEPT_LANGUAGE')
        self.accepted_encoding = environ.get('HTTP_ACCEPT_ENCODING')

    def is_get(self):
        return self.request_method == 'GET'

    def is_post(self):
        return self.request_method == 'POST'
