import hashlib
from typing import Annotated

from fastapi import Header, Request


def get_device_fingerprint(
    request: Request,
    user_agent: Annotated[str | None, Header(alias="User-Agent")] = None,
) -> str:
    """SHA-256 fingerprint from User-Agent (matches nest-core-clean device binding)."""
    raw = user_agent or request.headers.get("user-agent") or "unknown"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
