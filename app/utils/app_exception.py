from app.utils.error_codes import ErrorCode


class AppException(Exception):
    """Base application exception for controlled error responses."""

    def __init__(
        self,
        code: ErrorCode,
        status_code: int = 400,
        detail: list[str] | None = None,
    ):
        self.detail = detail or []
        self.code = code
        self.status_code = status_code
