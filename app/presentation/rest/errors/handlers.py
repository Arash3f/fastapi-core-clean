from datetime import UTC, datetime
from typing import cast

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.responses import Response

from app.presentation.rest.errors.error_resolver import resolve_message
from app.presentation.rest.utils.language import detect_language
from app.utils.app_exception import AppException


async def app_exception_handler(request: Request, exc: Exception) -> Response:
    app_exc = cast(AppException, exc)
    lang = detect_language(request)
    message_en = resolve_message(app_exc.code, "en")
    message_fa = resolve_message(app_exc.code, "fa")
    message = message_fa if lang == "fa" else message_en
    trace_id = getattr(request.state, "trace_id", None)

    return JSONResponse(
        status_code=app_exc.status_code,
        content={
            "path": request.url.path,
            "statusCode": app_exc.status_code,
            "code": app_exc.code.name,
            "message": message,
            "persianTranslation": message_fa,
            "timestamp": datetime.now(UTC).isoformat(),
            "trace_id": trace_id,
            "detail": app_exc.detail,
        },
    )
