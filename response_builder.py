from constants import HTTP_VERSION

class HTTPResponseBuilder:
    @staticmethod
    def build_response(status: str, content: bytes = b"", headers: str = "") -> bytes:
        """
        Builds HTTP response.
        :param status: The status of the response (e.g., 200 OK).
        :param  content: Body of the response.
        :param headers: Additional HTTP headers.
        :return: HTTP Response.
        """
        response = (
            f"{HTTP_VERSION} {status}\r\n"
            f"Content-Length: {len(content)}\r\n"
            f"{headers}"
            f"\r\n"
        ).encode() + content
        return response
    
    def convert_headers_to_raw_headers(headers: dict) -> str:
        """
        Converts formatted http headers into raw http heaers.
        :param headers: formatted http headers.
        :return: raw headers.
        """
        pass