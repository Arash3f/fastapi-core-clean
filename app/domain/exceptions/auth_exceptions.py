from app.utils.app_exception import AppException
from app.utils.error_codes import ErrorCode


class InvalidCredentialsException(AppException):
    def __init__(self, detail: list[str] | None = None):
        super().__init__(
            code=ErrorCode.INVALID_CREDENTIALS, status_code=401, detail=detail
        )


class InactiveUserException(AppException):
    def __init__(self, detail: list[str] | None = None):
        super().__init__(code=ErrorCode.INACTIVE_USER, status_code=403, detail=detail)


class InvalidRefreshTokenException(AppException):
    def __init__(self, detail: list[str] | None = None):
        super().__init__(
            code=ErrorCode.INVALID_REFRESH_TOKEN, status_code=401, detail=detail
        )


class DeviceMismatchException(AppException):
    def __init__(self, detail: list[str] | None = None):
        super().__init__(code=ErrorCode.DEVICE_MISMATCH, status_code=401, detail=detail)


class UserNotAuthorizedException(AppException):
    def __init__(self, detail: list[str] | None = None):
        super().__init__(
            code=ErrorCode.USER_NOT_AUTHORIZED, status_code=401, detail=detail
        )


class IncorrectCurrentPasswordException(AppException):
    def __init__(self, detail: list[str] | None = None):
        super().__init__(
            code=ErrorCode.INCORRECT_CURRENT_PASSWORD,
            status_code=400,
            detail=detail,
        )
