from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.shared.dto.user_filter_dto import FilterUserQuery
from app.domain.value_objects.role import Role


@dataclass
class CreateUserDTO:
    name: str
    username: str
    password: str
    role: Role = Role.MEMBER


@dataclass
class UpdateUserDTO:
    id: UUID
    name: str | None = None
    username: str | None = None
    role: Role | None = None
    active: bool | None = None


@dataclass
class UpdateMeDTO:
    user_id: UUID
    name: str | None = None
    username: str | None = None


@dataclass
class IdDTO:
    id: UUID


@dataclass
class UserResponseDTO:
    id: UUID
    username: str
    name: str
    active: bool
    role: Role
    created_at: datetime | None
    updated_at: datetime | None


@dataclass
class UserListResponseDTO:
    items: list[UserResponseDTO]
    total: int
    page: int
    page_size: int


# Re-export for use case convenience
FilterUsersDTO = FilterUserQuery
