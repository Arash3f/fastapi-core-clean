from datetime import datetime, timedelta, timezone
from uuid import UUID

from jose import jwt
from jose.exceptions import JWTError

from app.application.interfaces.token_service import (
    TokenPair,
    TokenPayload,
    TokenService,
)
from app.core.config import settings
from app.domain.value_objects.role import Role


class JWTService(TokenService):
    def sign_token_pair(
        self, *, user_id: UUID, username: str, device_id: str, role: Role
    ) -> TokenPair:
        base = {
            "id": str(user_id),
            "username": username.lower(),
            "deviceId": device_id,
            "role": role.value,
        }
        now = datetime.now(timezone.utc)

        access_payload = {
            **base,
            "type": "access",
            "exp": now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        refresh_payload = {
            **base,
            "type": "refresh",
            "exp": now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        }

        access = jwt.encode(
            access_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
        )
        refresh = jwt.encode(
            refresh_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
        )
        return TokenPair(access_token=access, refresh_token=refresh)

    def verify_access_token(self, token: str) -> TokenPayload:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        if payload.get("type") != "access":
            raise JWTError("not an access token")
        return self._to_payload(payload)

    def verify_refresh_token(self, token: str) -> TokenPayload:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        if payload.get("type") != "refresh":
            raise JWTError("not a refresh token")
        return self._to_payload(payload)

    def _to_payload(self, payload: dict) -> TokenPayload:
        return TokenPayload(
            id=UUID(payload["id"]),
            username=payload["username"],
            device_id=payload["deviceId"],
            role=Role(payload["role"]),
        )
