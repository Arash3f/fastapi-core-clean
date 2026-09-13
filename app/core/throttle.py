from fastapi import HTTPException, Request
from limits import parse
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import settings

limiter = Limiter(
    key_func=get_remote_address,
    enabled=not settings.is_test,
    default_limits=[],
)

_AUTH_LIMIT = parse(settings.auth_rate_limit)


def enforce_auth_rate_limit(request: Request) -> None:
    """Apply the shared auth rate limit (used by GraphQL resolvers)."""
    if settings.is_test or not limiter.enabled:
        return
    key = get_remote_address(request) or "anonymous"
    if not limiter.limiter.hit(_AUTH_LIMIT, key, "auth"):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
