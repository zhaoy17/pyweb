"""
This module provides utilities for parsing url string. Most of the implementation is based
on Python's urllib module with some slight modification. The incoming url is processed as
str, while the url consists in the outgoing url request will be processed using ASCII bytearray
"""
import re
from typing import Union

__all__ = [
    'to_string',
    'to_byte_array',
    'parse_query_string',
    'decode',
    'encode',
    'parse_host',
    'parse_path_info'
]

'''
reserved and unreserved chracter defined under the RFC 3986 (STD66): "Uniform Resource Identifiers" by T. Berners-Lee,
R. Fielding and L.  Masinter, January 2005.
'''
_ALPHA = frozenset(b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
_DIGIT = frozenset(b"0123456789")
_GEN_DELIMS = frozenset(b":/?#[]@")
_SUB_DELIMS = frozenset(b"!$&'()*+,;=")
_UNRESERVED = _ALPHA | _DIGIT | frozenset(b"-._~")
_RESERVED = _GEN_DELIMS | _SUB_DELIMS
_reg_hex = None
_reg_host = None

# lookup tables
_BYTE2HEX = {}
_HEX2BYTE = {}


def _urldecode(string: str) -> str:
    global _HEX2BYTE
    if str == "+":
        return " "
    string = string.lstrip('%')
    try:
        return _HEX2BYTE[string]
    except KeyError:
        _HEX2BYTE[string] = chr(int(string, 16))
        return _urldecode(string)


def _urlencode(byte: int) -> bytearray:
    global _BYTE2HEX
    if byte not in _UNRESERVED:
        try:
            return _BYTE2HEX[byte]
        except KeyError:
            _BYTE2HEX[byte] = to_byte_array('%{:02X}'.format(byte))
        return _urlencode(byte)
    else:
        return bytearray([byte])


'''
convert a string into a byte list. Skip all characters that are not in the range
of ISO/IEC 8859-1 character set to avoid undefined behavior

According to PEP3333, "Native" strings (which are always implemented using the type named str)
that are used for request/response headers and metadata". The content content of native strings
must be translatable to bytes via the Latin-1 encoding. HTTP does not support unicode.
'''


def to_byte_array(string: str) -> bytearray:
    byte_array = bytearray()
    for char in string:
        if ord(char) >= 256:
            continue
        else:
            byte_array.append(ord(char))
    return byte_array


'''
Convert a byte array into string
'''


def to_string(byte_array: Union[bytes, bytearray]) -> str:
    string = []
    for byte in byte_array:
        string.append(chr(byte))
    return "".join(string)


'''
Encode all characters in an url that does not belong to unreserved set of character into 
%hex representation of that character.
'''


def encode(bytes_array: Union[str, bytes, bytearray]) -> bytearray:
    if isinstance(bytes_array, str):
        bytes_array = to_byte_array(bytes_array)
    if isinstance(bytes_array, str):
        bytes_array = to_byte_array(bytes_array)
    return bytearray(b''.join([_urlencode(char) for char in bytes_array]))


def decode(string: Union[str, bytes, bytearray]) -> str:
    if isinstance(string, bytes) or isinstance(string, bytearray):
        string = to_string(string)
    if "%" not in string and "+" not in string:
        return string
    else:
        global _reg_hex
        if _reg_hex is None:
            _reg_hex = re.compile("(%[0-f][0-f])")
        string_list = _reg_hex.split(string)
        for index, item in enumerate(string_list):
            if len(item) > 0 and item[0] == "%":
                string_list[index] = _urldecode(item)
        return ''.join(string_list)


def parse_query_string(query: str) -> dict:
    pairs = query.split("&")
    kv = {}
    for item in pairs:
        key_value = item.split("=")
        # skip empty query string
        if len(key_value) == 1:
            continue
        elif len(key_value) != 2:
            raise ValueError("bad query field: {}".format(key_value))
        kv[decode(key_value[0].strip())] = decode(key_value[1].strip())
    return kv


def parse_path_info(string: str) -> list:
    string = decode(string.lstrip("/"))
    return string.split("/")


""" Implementation comes from urllib. Parse a canonical 'host:port' string into parts. 
Parse a host string (which may or may not contain a port) into
parts, taking into account that the string may contain
either a domain name or an IP address. In the latter case,
both IPv4 and IPv6 addresses are supported.
"""


def parse_host(host: str) -> tuple:
    global _reg_host
    if _reg_host is None:
        _reg_host = re.compile("(.*):([0-9]*)", re.DOTALL)
    match = _reg_host.fullmatch(host)
    if match:
        host, port = match.groups()
        if port:
            return host, int(port)
    return host, None
