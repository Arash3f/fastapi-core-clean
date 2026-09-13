from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.user import User
from app.domain.exceptions.user_exceptions import UserNotFoundException
from app.domain.shared.dto.pagination_dto import PaginatedResult
from app.domain.shared.dto.user_filter_dto import FilterUserQuery


class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User: ...

    @abstractmethod
    async def get(self, user_id: UUID) -> User | None: ...

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None: ...

    @abstractmethod
    async def get_list_by_filter(
        self, query: FilterUserQuery
    ) -> PaginatedResult[User]: ...

    @abstractmethod
    async def update(self, user: User) -> User: ...

    @abstractmethod
    async def soft_delete(self, user_id: UUID) -> None: ...

    @abstractmethod
    async def set_refresh_token_hash(
        self, user_id: UUID, refresh_token_hash: str | None
    ) -> None: ...

    @abstractmethod
    async def update_password(self, user_id: UUID, password_hash: str) -> None: ...

    async def get_or_raise(self, user_id: UUID) -> User:
        user = await self.get(user_id)
        if not user:
            raise UserNotFoundException(detail=[f"user id is {user_id}"])
        return user
