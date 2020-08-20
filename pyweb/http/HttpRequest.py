from .url import parse_query_string, parse_host, parse_path_info


class HTTPRequest:
    def __init__(self, environ):
        self._env = environ
        self.method = environ["REQUEST_METHOD"]
        try:
            self._pathinfo = environ["PATH_INFO"]
        except KeyError:
            self._pathinfo = "/"
        self.wsgi_error = environ["wsgi.errors"]
        self.wsgi_input = environ["wsgi.input"]
        self._query_string = None
        self._host = None
        self._port = None
        self._object_location = None
        self._content_type = None

    @property
    def query(self):
        try:
            raw_string = self._env["QUERY_STRING"] \
                .encode("latin1").decode("utf-8", "replace")
        except KeyError:
            raw_string = ""
        return raw_string

    @property
    def params(self):
        if not self._query_string:
            self._query_string = parse_query_string(self._env["QUERY_STRING"])
        return self._query_string

    @property
    def object_location(self):
        if self._object_location is None:
            self._object_location = parse_path_info(self._pathinfo)
        else:
            return self._object_location

    '''Return the port According to PEP3333, HTTP_HOST is present should be preferred over
    SEVER_NAME and SEVER_PORT variable'''

    @property
    def port(self):
        if self._port is None:
            try:
                host, port = parse_host(self._env['HTTP_HOST'])
                self._host = host
                if port is None:
                    self._port = 443 if self._env['wsgi.url_scheme'] == 'https' else 80
            except KeyError:
                self._host = self._env['SERVER_NAME']
                self._port = self._env['SERVER_PORT']
        return self._port

    @property
    def host(self):
        if self._host is None:
            self.port()
        return self._host

    @property
    def content_type(self):
        if self.method == "GET":
            return ""
