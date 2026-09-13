from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.domain.shared.dto.sorter_dto import SortOrderField
from app.domain.shared.dto.user_filter_dto import UserSortField
from app.domain.value_objects.role import Role


class SuccessResponse(BaseModel):
    success: bool = True


class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    page_size: int


class LoginRequest(BaseModel):
    username: str
    password: str = Field(min_length=1)


class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=4, max_length=128)


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ChangeMyPasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=4, max_length=128)


class ChangePasswordRequest(BaseModel):
    user_id: UUID
    new_password: str = Field(min_length=4, max_length=128)


class UserModel(BaseModel):
    id: UUID
    username: str
    name: str
    active: bool
    role: Role
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CreateUserRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=4, max_length=128)
    role: Role = Role.MEMBER


class UpdateUserRequest(BaseModel):
    id: UUID
    name: str | None = None
    username: str | None = None
    role: Role | None = None
    active: bool | None = None


class UpdateMeRequest(BaseModel):
    name: str | None = None
    username: str | None = None


class UserFiltersRequest(BaseModel):
    id: UUID | None = None
    username: str | None = None
    name: str | None = None
    role: Role | None = None
    active: bool | None = None


class ReadUsersRequest(BaseModel):
    filters: UserFiltersRequest | None = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    sort_by: UserSortField = UserSortField.CREATED_AT
    sort_order: SortOrderField = SortOrderField.DESC


class ReadUsersResponse(BaseModel):
    items: list[UserModel]
    total: int
    page: int
    page_size: int
