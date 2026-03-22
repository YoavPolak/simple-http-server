from datetime import datetime
from typing import Tuple
import logging

from constants import CONTENT_LENGTH_KEY, HTTP_HEADER_DELIMITER
from socketserver import BaseRequestHandler, TCPServer, ThreadingMixIn

from http_parser import HTTPParser
from http_request_handler import HTTPRequestHandler

class ThreadedTCPRequestHandler(BaseRequestHandler):
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
        except ValueError as response:
            self.request.sendall(str(response).encode())
            return
        content_length = int(headers.get(CONTENT_LENGTH_KEY, 0))
        body = self._receive_body(body, content_length)
        response = HTTPRequestHandler.handle(status, headers, body)
        self.request.sendall(response)
        self.logger.info(f'[{datetime.now()}] {self.client_address[0]} {headers.get("user-agent")}')


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

class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    pass