from collections.abc import Mapping
from enum import Enum
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User
from app.domain.exceptions.user_exceptions import UserNotFoundException
from app.domain.repositories.user_repository import UserRepository
from app.domain.shared.dto.pagination_dto import PaginatedResult
from app.domain.shared.dto.user_filter_dto import FilterUserQuery, UserSortField
from app.infrastructure.database.models.user_model import UserModel
from app.infrastructure.database.utils.pagination_and_sort import paginate_and_sort


class SQLUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        model = self._to_model(user)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def get(self, user_id: UUID) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_username(self, username: str) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.username == username.lower())
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_list_by_filter(self, query: FilterUserQuery) -> PaginatedResult[User]:
        stmt = select(UserModel)
        filters = query.filters

        if filters:
            if filters.username:
                stmt = stmt.where(UserModel.username.ilike(f"%{filters.username}%"))
            if filters.name:
                stmt = stmt.where(UserModel.name.ilike(f"%{filters.name}%"))
            if filters.id:
                stmt = stmt.where(UserModel.id == filters.id)
            if filters.role is not None:
                stmt = stmt.where(UserModel.role == filters.role)
            if filters.active is not None:
                stmt = stmt.where(UserModel.active == filters.active)

        SORTABLE_COLUMNS: Mapping[Enum, Any] = {
            UserSortField.ID: UserModel.id,
            UserSortField.USERNAME: UserModel.username,
            UserSortField.NAME: UserModel.name,
            UserSortField.CREATED_AT: UserModel.created_at,
        }

        result = await paginate_and_sort(
            model=UserModel,
            stmt=stmt,
            session=self.session,
            page=query.pagination.page,
            page_size=query.pagination.page_size,
            sort_by=query.sort.sort_by,
            offset=query.pagination.offset,
            sort_order=query.sort.sort_order,
            sortable_columns=SORTABLE_COLUMNS,
        )

        users = [self._to_entity(m) for m in result.items]
        return PaginatedResult[User](
            items=users,
            total=result.total,
            page=result.page,
            page_size=result.page_size,
        )

    async def update(self, user: User) -> User:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user.id)
        )
        model = result.scalar_one_or_none()
        if model is None:
            raise UserNotFoundException(detail=[f"user id is {user.id}"])

        model.username = user.username
        model.name = user.name
        model.active = user.active
        model.role = user.role
        model.password_hash = user.password_hash
        model.refresh_token_hash = user.refresh_token_hash

        await self.session.flush()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def soft_delete(self, user_id: UUID) -> None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        if model is None:
            raise UserNotFoundException(detail=[f"user id is {user_id}"])
        model.active = False
        await self.session.flush()

    async def set_refresh_token_hash(
        self, user_id: UUID, refresh_token_hash: str | None
    ) -> None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        if model is None:
            raise UserNotFoundException(detail=[f"user id is {user_id}"])
        model.refresh_token_hash = refresh_token_hash
        await self.session.flush()

    async def update_password(self, user_id: UUID, password_hash: str) -> None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        if model is None:
            raise UserNotFoundException(detail=[f"user id is {user_id}"])
        model.password_hash = password_hash
        await self.session.flush()

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            username=model.username,
            password_hash=model.password_hash,
            name=model.name,
            active=model.active,
            role=model.role,
            refresh_token_hash=model.refresh_token_hash,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            username=entity.username,
            password_hash=entity.password_hash,
            name=entity.name,
            active=entity.active,
            role=entity.role,
            refresh_token_hash=entity.refresh_token_hash,
        )
