import logging

from app.infrastructure.utils.context import get_trace_id


class ContextTraceFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = get_trace_id() or "-"
        return True


def configure_logging() -> None:
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | trace_id=%(trace_id)s | %(message)s"
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.addFilter(ContextTraceFilter())

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    if not root_logger.handlers:
        root_logger.addHandler(handler)
