from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from app.domain.value_objects.role import Role


@dataclass
class TokenPayload:
    id: UUID
    username: str
    device_id: str
    role: Role


@dataclass
class TokenPair:
    access_token: str
    refresh_token: str


class TokenService(ABC):
    @abstractmethod
    def sign_token_pair(
        self, *, user_id: UUID, username: str, device_id: str, role: Role
    ) -> TokenPair:
        pass

    @abstractmethod
    def verify_access_token(self, token: str) -> TokenPayload:
        pass

    @abstractmethod
    def verify_refresh_token(self, token: str) -> TokenPayload:
        pass
