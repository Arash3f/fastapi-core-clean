from app.utils.app_exception import AppException
from app.utils.error_codes import ErrorCode


class UserNotFoundException(AppException):
    def __init__(self, detail: list[str] | None = None):
        super().__init__(code=ErrorCode.USER_NOT_FOUND, status_code=404, detail=detail)


class UsernameDuplicatedException(AppException):
    def __init__(self, detail: list[str] | None = None):
        super().__init__(
            code=ErrorCode.USERNAME_DUPLICATED, status_code=409, detail=detail
        )


class ForbiddenException(AppException):
    def __init__(self, detail: list[str] | None = None):
        super().__init__(code=ErrorCode.FORBIDDEN, status_code=403, detail=detail)
