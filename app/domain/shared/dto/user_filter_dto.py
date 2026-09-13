from enum import Enum
from uuid import UUID

from pydantic import BaseModel

from app.domain.shared.dto.pagination_dto import PaginationParams
from app.domain.shared.dto.sorter_dto import SortParams
from app.domain.value_objects.role import Role


class UserSortField(str, Enum):
    ID = "id"
    USERNAME = "username"
    NAME = "name"
    CREATED_AT = "created_at"


class UserFilters(BaseModel):
    id: UUID | None = None
    username: str | None = None
    name: str | None = None
    role: Role | None = None
    active: bool | None = None


class FilterUserQuery(BaseModel):
    filters: UserFilters | None = None
    pagination: PaginationParams = PaginationParams()
    sort: SortParams[UserSortField] = SortParams(sort_by=UserSortField.CREATED_AT)
