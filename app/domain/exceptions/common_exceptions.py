from app.utils.app_exception import AppException
from app.utils.error_codes import ErrorCode


class UnexpectedIdException(AppException):
    def __init__(self, detail: list[str] | None = None):
        super().__init__(code=ErrorCode.UN_EXPECTED_ID, status_code=500, detail=detail)


class InvalidPageException(AppException):
    def __init__(self, detail: list[str] | None = None):
        super().__init__(code=ErrorCode.INVALID_PAGE, status_code=400, detail=detail)


class InvalidPageSizeException(AppException):
    def __init__(self, detail: list[str] | None = None):
        super().__init__(
            code=ErrorCode.INVALID_PAGE_SIZE, status_code=400, detail=detail
        )
