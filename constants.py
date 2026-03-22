BAD_REQUEST = b"""
HTTP/1.1 400 Bad Request\r\n
Content-Type: text/plain\r\n
Content-Length: 11\r\n
\r\n
Bad Request
"""

NOT_FOUND = b"HTTP/1.1 404 Not Found\r\n\r\nFile not found"
CONTENT_LENGTH_KEY = "content-length"
HTTP_HEADER_DELIMITER = "\r\n\r\n"
METHODS = ["GET", "POST"]
HTTP_VERSION = "HTTP/1.1"