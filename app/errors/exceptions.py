from starlette import status

from errors import APIErrorSchema


class APIException(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    error_code: str = "bad_request"
    message: str = "Something went wrong"
    debug: str | None = None

    def __init__(self, message: str | None = None, debug: str | None = None):
        self.message = message or self.message
        self.debug = debug or self.debug

    def to_pydantic(self, debug_mode: bool = False) -> APIErrorSchema:
        return APIErrorSchema(
            error_code=self.error_code,
            message=self.message,
            debug=self.debug if debug_mode else None,
        )


class ForbiddenAccess(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "forbidden"
    message = "You don’t have permission to perform this action."


class ObjectNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "not_found"
    message = "The requested resource was not found."


class EmailServiceError(APIException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code: str = "email_service"
    message: str = "Something went wrong with email service"
