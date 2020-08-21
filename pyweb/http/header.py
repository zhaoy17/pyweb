"""
This module consists of functions that are used to parse multipart and discrete
MIME header.
"""

__all__ = [
    'parse_content_type',
    'extension_to_header',
    'header_to_extension',
    'types_supported',
    'handleContent'
]

extension_to_header = {
    '.js': 'application/javascript',
    '.mjs': 'application/javascript',
    '.json': 'application/json',
    '.webmanifest': 'application/manifest+json',
    '.doc': 'application/msword',
    '.dot': 'application/msword',
    '.wiz': 'application/msword',
    '.bin': 'application/octet-stream',
    '.a': 'application/octet-stream',
    '.dll': 'application/octet-stream',
    '.exe': 'application/octet-stream',
    '.o': 'application/octet-stream',
    '.obj': 'application/octet-stream',
    '.so': 'application/octet-stream',
    '.oda': 'application/oda',
    '.pdf': 'application/pdf',
    '.p7c': 'application/pkcs7-mime',
    '.ps': 'application/postscript',
    '.ai': 'application/postscript',
    '.eps': 'application/postscript',
    '.m3u': 'application/vnd.apple.mpegurl',
    '.m3u8': 'application/vnd.apple.mpegurl',
    '.xls': 'application/vnd.ms-excel',
    '.xlb': 'application/vnd.ms-excel',
    '.ppt': 'application/vnd.ms-powerpoint',
    '.pot': 'application/vnd.ms-powerpoint',
    '.ppa': 'application/vnd.ms-powerpoint',
    '.pps': 'application/vnd.ms-powerpoint',
    '.pwz': 'application/vnd.ms-powerpoint',
    '.wasm': 'application/wasm',
    '.bcpio': 'application/x-bcpio',
    '.cpio': 'application/x-cpio',
    '.csh': 'application/x-csh',
    '.dvi': 'application/x-dvi',
    '.gtar': 'application/x-gtar',
    '.hdf': 'application/x-hdf',
    '.h5': 'application/x-hdf5',
    '.latex': 'application/x-latex',
    '.mif': 'application/x-mif',
    '.cdf': 'application/x-netcdf',
    '.nc': 'application/x-netcdf',
    '.p12': 'application/x-pkcs12',
    '.pfx': 'application/x-pkcs12',
    '.ram': 'application/x-pn-realaudio',
    '.pyc': 'application/x-python-code',
    '.pyo': 'application/x-python-code',
    '.sh': 'application/x-sh',
    '.shar': 'application/x-shar',
    '.swf': 'application/x-shockwave-flash',
    '.sv4cpio': 'application/x-sv4cpio',
    '.sv4crc': 'application/x-sv4crc',
    '.tar': 'application/x-tar',
    '.tcl': 'application/x-tcl',
    '.tex': 'application/x-tex',
    '.texi': 'application/x-texinfo',
    '.texinfo': 'application/x-texinfo',
    '.roff': 'application/x-troff',
    '.t': 'application/x-troff',
    '.tr': 'application/x-troff',
    '.man': 'application/x-troff-man',
    '.me': 'application/x-troff-me',
    '.ms': 'application/x-troff-ms',
    '.ustar': 'application/x-ustar',
    '.src': 'application/x-wais-source',
    '.xsl': 'application/xml',
    '.rdf': 'application/xml',
    '.wsdl': 'application/xml',
    '.xpdl': 'application/xml',
    '.zip': 'application/zip',
    '.au': 'audio/basic',
    '.snd': 'audio/basic',
    '.mp3': 'audio/mpeg',
    '.mp2': 'audio/mpeg',
    '.aif': 'audio/x-aiff',
    '.aifc': 'audio/x-aiff',
    '.aiff': 'audio/x-aiff',
    '.ra': 'audio/x-pn-realaudio',
    '.wav': 'audio/x-wav',
    '.gif': 'image/gif',
    '.ief': 'image/ief',
    '.jpg': 'image/jpeg',
    '.jpe': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.svg': 'image/svg+xml',
    '.tiff': 'image/tiff',
    '.tif': 'image/tiff',
    '.ico': 'image/vnd.microsoft.icon',
    '.ras': 'image/x-cmu-raster',
    '.bmp': 'image/x-ms-bmp',
    '.pnm': 'image/x-portable-anymap',
    '.pbm': 'image/x-portable-bitmap',
    '.pgm': 'image/x-portable-graymap',
    '.ppm': 'image/x-portable-pixmap',
    '.rgb': 'image/x-rgb',
    '.xbm': 'image/x-xbitmap',
    '.xpm': 'image/x-xpixmap',
    '.xwd': 'image/x-xwindowdump',
    '.eml': 'message/rfc822',
    '.mht': 'message/rfc822',
    '.mhtml': 'message/rfc822',
    '.nws': 'message/rfc822',
    '.css': 'text/css',
    '.csv': 'text/csv',
    '.html': 'text/html',
    '.htm': 'text/html',
    '.txt': 'text/plain',
    '.bat': 'text/plain',
    '.c': 'text/plain',
    '.h': 'text/plain',
    '.ksh': 'text/plain',
    '.pl': 'text/plain',
    '.rtx': 'text/richtext',
    '.tsv': 'text/tab-separated-values',
    '.py': 'text/x-python',
    '.etx': 'text/x-setext',
    '.sgm': 'text/x-sgml',
    '.sgml': 'text/x-sgml',
    '.vcf': 'text/x-vcard',
    '.xml': 'text/xml',
    '.mp4': 'video/mp4',
    '.mpeg': 'video/mpeg',
    '.m1v': 'video/mpeg',
    '.mpa': 'video/mpeg',
    '.mpe': 'video/mpeg',
    '.mpg': 'video/mpeg',
    '.mov': 'video/quicktime',
    '.qt': 'video/quicktime',
    '.webm': 'video/webm',
    '.avi': 'video/x-msvideo',
    '.movie': 'video/x-sgi-movie',
}

types_supported = {".json"}  # TODO add support for a greater variety of file types

header_to_extension = {}

for ext in extension_to_header:
    if extension_to_header[ext] not in header_to_extension:
        header_to_extension[extension_to_header[ext]] = {ext}
    else:
        header_to_extension[extension_to_header[ext]].add(ext)

_accept = frozenset(extension_to_header[media].split("/")[1] for media in extension_to_header)


def parse_content_type(line: str, accepted_content_type: set = _accept) -> list:
    """Parse a Content-type like header.
    Return the main content-type and a dictionary of options.
    """
    if line == "":
        return ["", {}]
    parts = line.split(";")
    file_type_header = parts[0].lower().strip()
    if "/" in file_type_header:
        if file_type_header.split("/")[1] not in accepted_content_type:
            raise ValueError("unknown content type")
    elif file_type_header not in accepted_content_type:
        raise ValueError("unknown content type")
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


def handleContent(filetype, handler=None):
    if handler is None:
        try:
            return globals()["handle_" + filetype[1:]]
        except KeyError:
            raise ValueError("this filetype is not supported")
    else:
        try:
            return getattr(handler, filetype[1:])
        except KeyError:
            raise ValueError("this file type is not supported")


def handle_json(file):
    import json
    return json.loads(file)
