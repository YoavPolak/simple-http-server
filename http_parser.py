from io import StringIO

from constants import BAD_REQUEST, HTTP_VERSION, METHODS

class HTTPParser:
    @staticmethod
    def parse_headers(headers: str):
        """
        parse an http requests into the status-line and headers
        :param headers: Raw HTTP header.
        :return: HTTP Headers in dict format and HTTP status-line.
        """
        headers = StringIO(headers)
        status = headers.readline().strip()
        formatted_headers = {}
        for line in headers:
            line = line.strip()
            if ':' not in line:
                raise ValueError(BAD_REQUEST)
            key, value = line.split(':', 1)
            key, value = key.strip(), value.strip()
            if not key:
                raise ValueError(BAD_REQUEST)
            formatted_headers[key.lower()] = value
        return status, formatted_headers

    @staticmethod
    def parse_status(status: str):
        """
        Parse status-line into Method, Path and Version.
        :param status: status-line.
        :return: status-line as list.
        """
        status = status.split()
        if 3 != len(status):
            raise ValueError(BAD_REQUEST)
        if status[0] not in METHODS and not status[1].startswith('/') and HTTP_VERSION != status[2]:
            raise ValueError(BAD_REQUEST)
        return status
    
    @staticmethod
    def parse_body(body: str):
        pass