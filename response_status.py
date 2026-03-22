from enum import StrEnum

class ResponseStatus(StrEnum):
    OK = "200 OK"
    BAD_REQUEST = "400 Bad Request"
    NOT_FOUND = "404 Not Found"