"""
This module consists of functions that are used to parse multipart and discrete
MIME header.
"""

from abc import ABC, abstractmethod
import json

__all__ = [
    "ContentType",
    "Header",
    "HTTPBody"
]


class Header(ABC):
    @abstractmethod
    def to_str(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @abstractmethod
    def __bool__(self):
        pass

    @abstractmethod
    def to_header(self) -> str:
        pass

    @abstractmethod
    def to_list(self) -> list:
        pass


class ContentType(Header):
    class Handler(ABC):
        @abstractmethod
        def parse(self):
            pass

        @staticmethod
        @abstractmethod
        def content_type() -> list:
            pass

    class JSONHandler(Handler):
        def __init__(self, raw_string: str):
            self._str = raw_string
            self._dict = None

        def to_str(self) -> str:
            return self._str

        def parse(self) -> dict:
            if self._dict is None:
                self._dict = json.loads(self._str)
            return self._dict

        @staticmethod
        def content_type() -> list:
            return ["application/json"]

    _HandlerMap = {"application/json": JSONHandler}

    def __init__(self, raw_header):
        self._raw = raw_header
        self._str = None
        self._dict = None
        self._bool = None
        self._list = None

    def to_header(self):
        return self._raw

    def to_str(self) -> str:
        if not self:
            return ""
        if self._str is None:
            self._str = self._raw.split(";")[0]
        return self._str

    def to_dict(self) -> dict:
        if not self:
            return {}
        if self._dict is None:
            if self._list is None:
                self._list = self._parse_content_type(self._str)
            content = self._list[0]
            params = self._list[1]
            params["type"] = content
            self._dict = params
        return self._dict

    def __bool__(self):
        return self._str != ""

    def to_list(self):
        if not self:
            return None
        if self._dict is None:
            self.to_dict()
        return self._dict.keys()

    @classmethod
    def from_dict(cls, content_type: dict):
        charset = "utf-8"
        if "charset" in content_type:
            charset = content_type["charset"]
        raw_header = content_type["type"] + "; " + charset
        for key in content_type:
            if key != "charset":
                raw_header += "; " + content_type[key]
        return cls(raw_header)

    def get_handler(self, raw_string: str) -> Handler:
        content_type = self.to_str()
        try:
            return ContentType._HandlerMap[content_type](raw_string)
        except KeyError:
            raise ValueError("Header type not supported")

    @staticmethod
    def add_handler(handler: Handler):
        for _t in handler.content_type():
            ContentType._HandlerMap[_t] = handler

    @staticmethod
    def _parse_content_type(line: str) -> list:
        """Parse a Content-type like header.
        Return the main content-type and a dictionary of options.
        """
        if line == "":
            return ["", {}]
        parts = line.split(";")
        file_type_header = parts[0].lower().strip()
        content = file_type_header
        params = {}
        if len(parts) > 1:
            for i in range(1, len(parts)):
                kv = parts[i].split("=")
                if len(kv) != 2:
                    raise ValueError("content-type header is not formatted correctly")
                else:
                    params[kv[0].strip()] = kv[1].strip()
        return [content, params]


class HTTPBody:
    def __init__(self, stream, content_type: ContentType, content_length: int):
        self._content_type = content_type
        self._input = stream
        try:
            self._encoding = content_type.to_dict()["charset"]
        except KeyError:
            self._encoding = "utf-8"
        self._handler = None
        self._data = None
        self._str = None
        self._output = None
        self._size = content_length

    def get_bytes(self):
        if self._data is None:
            self._data = self._input.read(self._size)
        return self._data

    def get_str(self):
        if self._str is None:
            self._str = self.get_bytes().decode(self._encoding)
        return self._str

    def parse_content(self):
        if self._output is None:
            if self._handler is None:
                self._handler = self._content_type.get_handler(self.get_str())
                self._output = self._handler.parse()
        return self._output
