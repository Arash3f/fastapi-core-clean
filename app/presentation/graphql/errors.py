from graphql import GraphQLError
from starlette.requests import Request

from app.presentation.rest.errors.error_resolver import resolve_message
from app.presentation.rest.utils.language import detect_language
from app.utils.app_exception import AppException


def raise_graphql_app_exception(exc: AppException, request: Request | None) -> None:
    lang = detect_language(request) if request is not None else "en"
    message_en = resolve_message(exc.code, "en")
    message_fa = resolve_message(exc.code, "fa")
    message = message_fa if lang == "fa" else message_en
    trace_id = getattr(request.state, "trace_id", None) if request is not None else None

    raise GraphQLError(
        message,
        extensions={
            "path": request.url.path if request is not None else "/graphql",
            "statusCode": exc.status_code,
            "code": exc.code.name,
            "message": message,
            "persianTranslation": message_fa,
            "trace_id": trace_id,
            "detail": exc.detail,
        },
    ) from exc
