from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.exceptions.common_exceptions import UnexpectedIdException
from app.domain.value_objects.role import Role


@dataclass
class User:
    username: str
    password_hash: str
    name: str
    active: bool
    role: Role
    refresh_token_hash: str | None = None
    id: UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @property
    def safe_id(self) -> UUID:
        if self.id is None:
            raise UnexpectedIdException(detail=[f"user username={self.username}"])
        return self.id
