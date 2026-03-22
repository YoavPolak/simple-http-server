from datetime import datetime
from http import HTTPStatus
from typing import Tuple
import logging

from constants import HTTP_HEADER_DELIMITER
from socketserver import BaseRequestHandler, TCPServer, ThreadingMixIn

from http_headers import HTTPHeaders
from http_parser import HTTPParser
from http_request_handler import HTTPRequestHandler
from http_response_handler import HTTPResponseHandler

class HTTPServerHandler(BaseRequestHandler):
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    def handle(self):
        """
        Handle Socket IO and main logic
        for http requests and responses.
        """
        headers, body = self._receive_headers()
        try:
            status, headers = HTTPParser.parse_headers(headers)
            status = HTTPParser.parse_status(status)
        except ValueError as response_message:
            self.request.sendall(HTTPResponseHandler.build_response(HTTPStatus.BAD_REQUEST, str(response_message).encode()))
            return
        content_length = int(headers.get(HTTPHeaders.CONTENT_LENGTH, 0))
        body = self._receive_body(body, content_length)
        response = HTTPRequestHandler.handle(status, headers, body)
        self.request.sendall(response)
        self.logger.info(f'[{datetime.now()}] {self.client_address[0]} {headers.get(HTTPHeaders.USER_AGENT)}')


    def _receive_headers(self) -> Tuple[str, str]:
        """
        Receive raw http headers.
        :return: Tuple of raw headers and raw body.
        """
        buffer = ""
        while HTTP_HEADER_DELIMITER not in buffer:
            chunk = self.request.recv(1024).decode()
            if not chunk:
                break
            buffer += chunk
        
        return buffer.split(HTTP_HEADER_DELIMITER, 1)
    
    def _receive_body(self, body: str, content_length: int) -> str:
        """
        Receive remainings of http body.
        :return: raw body.
        """
        while len(body) < content_length:
            body += self.request.recv(1024).decode()
        return body

class HTTPServer(ThreadingMixIn, TCPServer):
    pass