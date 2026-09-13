from app.application.dto.user_dto import UpdateMeDTO, UserResponseDTO
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.use_cases.user.create_user_use_case import _to_response
from app.domain.exceptions.user_exceptions import (
    UsernameDuplicatedException,
    UserNotFoundException,
)


class UpdateMeUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, data: UpdateMeDTO) -> UserResponseDTO:
        async with self.uow:
            user = await self.uow.users.get(data.user_id)
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

            updated = await self.uow.users.update(user)
            await self.uow.commit()
            return _to_response(updated)
