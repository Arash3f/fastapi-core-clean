from app.application.dto.user_dto import UpdateUserDTO, UserResponseDTO
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.use_cases.user.create_user_use_case import _to_response
from app.domain.exceptions.user_exceptions import (
    UsernameDuplicatedException,
    UserNotFoundException,
)


class UpdateUserUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, data: UpdateUserDTO) -> UserResponseDTO:
        async with self.uow:
            user = await self.uow.users.get(data.id)
            if not user:
                raise UserNotFoundException()

            if data.username is not None:
                username = data.username.lower().strip()
                existing = await self.uow.users.get_by_username(username)
                if existing and existing.safe_id != user.safe_id:
                    raise UsernameDuplicatedException()
                user.username = username

            if data.name is not None:
                user.name = data.name.strip()

            if data.role is not None:
                user.role = data.role

            if data.active is not None:
                user.active = data.active
                if not data.active:
                    user.refresh_token_hash = None

            updated = await self.uow.users.update(user)
            await self.uow.commit()
            return _to_response(updated)
