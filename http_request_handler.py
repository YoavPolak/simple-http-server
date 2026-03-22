import os

from constants import NOT_FOUND
from http_response_handler import HTTPResponseHandler
from response_status import ResponseStatus

class HTTPRequestHandler:
    @staticmethod
    def handle(status, headers, body) -> bytes:
        """
        Handles incoming http requests.
        :param headers: Request headers
        :param body: Request body
        :return: HTTP Response
        """
        method = status[0]
        handler = HTTPRequestHandler.METHOD_HANDLERS.get(method)
        if handler:
            return handler(status, headers, body)
        else:
            return HTTPRequestHandler.handle_unknown(status, headers, body)

    @staticmethod
    def handle_get_request(status, headers, body) -> bytes:
        """
        Handles a GET request.
        :param status: Contains the http method of the request
        :param headers: Request headers
        :param body: Request body
        :return: HTTP Response
        """
        path = status[1].split("?")[0]
        path = path.lstrip("/")
        requested_path = os.path.join(os.getcwd(), path)
        requested_path = os.path.abspath(requested_path)
        if os.path.isfile(requested_path):
            with open(requested_path, "rb") as fd:
                content = fd.read()
                return HTTPResponseHandler.build_response(ResponseStatus.OK, content)
        elif os.path.isdir(requested_path):
            content = "\n".join(os.listdir(requested_path)).encode()
            return HTTPResponseHandler.build_response(ResponseStatus.OK, content)
        return HTTPResponseHandler.build_response(ResponseStatus.NOT_FOUND, NOT_FOUND)

    @staticmethod
    def handle_post_request(status, headers, body):
        """
        Handles a POST request.
        :param status: Contains the http method of the request
        :param headers: Request headers
        :param body: Request body
        :return: HTTP Response
        """

    @staticmethod
    def handle_unknown(status, headers, body):
        pass

HTTPRequestHandler.METHOD_HANDLERS = {
    "GET": HTTPRequestHandler.handle_get_request,
    "POST": HTTPRequestHandler.handle_post_request
}