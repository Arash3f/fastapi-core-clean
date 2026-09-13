from datetime import datetime
from enum import Enum
from uuid import UUID

import strawberry

from app.domain.value_objects.role import Role as DomainRole


@strawberry.enum
class RoleGql(Enum):
    Admin = "Admin"
    Member = "Member"

    @classmethod
    def from_domain(cls, role: DomainRole) -> "RoleGql":
        return cls.Admin if role == DomainRole.ADMIN else cls.Member

    def to_domain(self) -> DomainRole:
        return DomainRole.ADMIN if self == RoleGql.Admin else DomainRole.MEMBER


@strawberry.type
class TokenType:
    access_token: str
    refresh_token: str


@strawberry.type
class SuccessType:
    success: bool


@strawberry.type
class UserType:
    id: UUID
    username: str
    name: str
    active: bool
    role: RoleGql
    created_at: datetime | None
    updated_at: datetime | None


@strawberry.type
class UserListType:
    items: list[UserType]
    total: int
    page: int
    page_size: int


@strawberry.input
class RegisterInput:
    name: str
    username: str
    password: str


@strawberry.input
class LoginInput:
    username: str
    password: str


@strawberry.input
class RefreshTokenInput:
    refresh_token: str


@strawberry.input
class ChangeMyPasswordInput:
    current_password: str
    new_password: str


@strawberry.input
class ChangePasswordInput:
    user_id: UUID
    new_password: str


@strawberry.input
class CreateUserInput:
    name: str
    username: str
    password: str
    role: RoleGql = RoleGql.Member


@strawberry.input
class UpdateMeInput:
    name: str | None = None
    username: str | None = None


@strawberry.input
class UpdateUserInput:
    id: UUID
    name: str | None = None
    username: str | None = None
    role: RoleGql | None = None
    active: bool | None = None


@strawberry.input
class UserFiltersInput:
    username: str | None = None
    name: str | None = None
    role: RoleGql | None = None
    active: bool | None = None


@strawberry.input
class ReadUsersInput:
    filters: UserFiltersInput | None = None
    page: int = 1
    page_size: int = 20
