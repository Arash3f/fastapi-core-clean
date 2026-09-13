import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.infrastructure.utils.context import trace_id_context


class TraceIDMiddleware(BaseHTTPMiddleware):
    TRACE_HEADER = "X-Trace-ID"

    async def dispatch(self, request: Request, call_next) -> Response:
        trace_id = request.headers.get(self.TRACE_HEADER) or str(uuid.uuid4())
        request.state.trace_id = trace_id
        token = trace_id_context.set(trace_id)
        try:
            response: Response = await call_next(request)
            response.headers[self.TRACE_HEADER] = trace_id
            return response
        finally:
            trace_id_context.reset(token)
