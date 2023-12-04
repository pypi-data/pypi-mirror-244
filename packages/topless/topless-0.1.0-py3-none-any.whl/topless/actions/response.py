import json
from http import HTTPStatus
from typing import Dict, List, Union

from topless.errors import ErrorCode
from topless.schemas import BaseSchema


class Response:
    def __init__(
        self, status_code: HTTPStatus = HTTPStatus.OK, body: str = "", headers=None
    ) -> None:
        self.statusCode = status_code.value
        self.headers = self.initialize_headers(headers)
        self.body = self.initialize_body(body)

    def initialize_headers(self, headers):
        initial_headers = {"Access-Control-Allow-Origin": "*"}

        if headers and isinstance(headers, dict):
            initial_headers.update(headers)
        return initial_headers

    def initialize_body(self, body):
        if not body or body == "":
            return ""

        if isinstance(body, BaseSchema):
            return self.process_schema_body(body)

        if isinstance(body, list):
            return self.process_list_body(body)

        if isinstance(body, dict):
            return self.process_dict_body(body)

        return json.dumps({"data": body}, ensure_ascii=False)

    def process_schema_body(self, body):
        return json.dumps({"data": body.dump()}, ensure_ascii=False)

    def process_list_body(self, body):
        new_list = [
            item.dump() if isinstance(item, BaseSchema) else item for item in body
        ]
        return json.dumps({"data": new_list}, ensure_ascii=False)

    def process_page_body(self, body):
        response_body = {
            "data": [item.dump() for item in body.items],
            "page": body.dump(),
        }
        return json.dumps(response_body, ensure_ascii=False)

    def process_dict_body(self, body):
        if body.get("data") or body.get("errors"):
            return json.dumps(body, ensure_ascii=False)

        return json.dumps({"data": body}, ensure_ascii=False)

    def dump(self):
        return self.__dict__

    @classmethod
    def ok(cls, data={}):
        return cls(HTTPStatus.OK, data)

    @classmethod
    def created(cls, data={}):
        return cls(HTTPStatus.CREATED, data)

    @classmethod
    def accepted(cls, data={}):
        return cls(HTTPStatus.ACCEPTED, data)

    @classmethod
    def no_content(cls):
        return cls(HTTPStatus.NO_CONTENT)

    @classmethod
    def forbidden(cls, message: str = None):
        message = message or "You shall not pass!"

        error = {"errors": [{"code": ErrorCode.FORBIDDEN, "message": message}]}

        return cls(HTTPStatus.FORBIDDEN, error)

    @classmethod
    def internal_server_error(cls, message: str = None):
        message = message or "An unexpected error has occurred."

        error = {
            "errors": [{"code": ErrorCode.INTERNAL_SERVER_ERROR, "message": message}]
        }

        return cls(HTTPStatus.INTERNAL_SERVER_ERROR, error)

    @classmethod
    def bad_request(
        cls, message: Union[Dict[str, str], str] = None, code: str = None
    ) -> Dict[str, List]:
        message = message or "Bad Request"
        code = code or ErrorCode.BAD_REQUEST

        error = {"errors": [{"code": code, "message": message}]}

        return cls(HTTPStatus.BAD_REQUEST, error)

    @classmethod
    def not_found(cls, message: str = None) -> Dict[str, List]:
        message = message or "Resource not found"

        error = {"errors": [{"code": "not-found", "message": message}]}

        return cls(HTTPStatus.NOT_FOUND, error)
