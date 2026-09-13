from contextvars import ContextVar

trace_id_context: ContextVar[str] = ContextVar("trace_id", default="-")


def set_trace_id(trace_id: str):
    trace_id_context.set(trace_id)


def get_trace_id() -> str:
    return trace_id_context.get("-")
