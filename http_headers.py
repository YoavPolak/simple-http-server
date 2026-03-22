from enum import StrEnum

class HTTPHeaders(StrEnum):
    CONTENT_LENGTH = "content-length"
    CONTENT_TYPE = "content-type"
    USER_AGENT = "user-agent"