from app.application.dto.user_dto import UserListResponseDTO, UserResponseDTO
from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.shared.dto.user_filter_dto import FilterUserQuery


class ReadUsersWithFilterUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, query: FilterUserQuery) -> UserListResponseDTO:
        async with self.uow:
            result = await self.uow.users.get_list_by_filter(query)

            items = [
                UserResponseDTO(
                    id=u.safe_id,
                    username=u.username,
                    name=u.name,
                    active=u.active,
                    role=u.role,
                    created_at=u.created_at,
                    updated_at=u.updated_at,
                )
                for u in result.items
            ]

            return UserListResponseDTO(
                items=items,
                total=result.total,
                page=result.page,
                page_size=result.page_size,
            )
