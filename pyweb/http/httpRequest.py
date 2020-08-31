from ._url import parse_query_string, parse_host, parse_path_info, decode
from .header import ContentType, HTTPBody


class BaseRequest:
    def __init__(self, environ):
        self._env = environ
        self._method = environ["REQUEST_METHOD"]
        try:
            self._pathinfo = environ["PATH_INFO"]
        except KeyError:
            self._pathinfo = "/"
        self._wsgi_error = environ["wsgi.errors"]
        self._stream = environ["wsgi.input"]
        self._host = None
        self._port = None
        self._path = None
        self._content_type = None
        self._query_string = None

    @property
    def method(self):
        return self._method

    @property
    def port(self):
        """
        infer the port number of the request; HTTP_HOST should be preferred over
        SEVER_NAME and SEVER_PORT variable according to PEP3333

        :return: the port number of the request as int
        """
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
    def host(self) -> str:
        if self._host is None:
            self.port()
        return self._host

    @property
    def path(self) -> list:
        if self._path is None:
            self._path = parse_path_info(self._pathinfo)
        return self._path

    @property
    def query_string(self) -> dict:
        if self._query_string is None:
            try:
                raw_string = self._env["QUERY_STRING"] \
                    .encode("latin1").decode("utf-8", "replace")
            except KeyError:
                raw_string = ""
            self._query_string = parse_query_string(raw_string)
        return self._query_string

    @property
    def content_type(self) -> ContentType:
        if self.method == "GET":
            return ContentType("")
        if self._content_type is None:
            try:
                header = decode(self._env["CONTENT_TYPE"]
                                .encode("latin1").decode("utf-8", "replace"))
            except KeyError:
                header = ""
            self._content_type = ContentType(header)
        return self._content_type

    @property
    def content_length(self) -> int:
        try:
            return self._env['CONTENT_LENGTH']
        except KeyError:
            return 0

    @property
    def message_body(self) -> HTTPBody:
        return HTTPBody(self._stream, self.content_type, self.content_length)
