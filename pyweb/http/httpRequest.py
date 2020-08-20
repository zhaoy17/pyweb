from typing import Callable
from .url import parse_query_string, parse_host, parse_path_info
from .header import parse_content_type, types_map


class HTTPRequest:
    def __init__(self, environ: dict):
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
    def query(self) -> str:
        try:
            raw_string = self._env["QUERY_STRING"] \
                .encode("latin1").decode("utf-8", "replace")
        except KeyError:
            raw_string = ""
        return raw_string

    @property
    def params(self) -> dict:
        if self._query_string is None:
            self._query_string = parse_query_string(self._env["QUERY_STRING"])
        return self._query_string

    @property
    def object_location(self) -> list:
        if self._object_location is None:
            self._object_location = parse_path_info(self._pathinfo)
        else:
            return self._object_location

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
    def content_type(self) -> list:
        if self.method == "GET":
            return ["", {}]
        if self._content_type is None:
            try:
                header = self._env["CONTENT_TYPE"]
            except KeyError:
                header = ""
            self._content_type = parse_content_type(header)
        return self._content_type

    @property
    def content_length(self) -> int:
        try:
            return self._env['CONTENT_LENGTH']
        except KeyError:
            return -1

    @property
    def content_extension(self) -> str:
        try:
            return types_map[self.content_type[0]]
        except KeyError:
            return ""

    def get_header(self, header: str, parser: Callable = None) -> str:
        try:
            output_header = self._env["HTTP_" + header.strip().upper()]
        except KeyError:
            raise ValueError("requires header: {}".format(header.strip().upper()))
        if parser is not None:
            return parser(output_header)
        else:
            return output_header
