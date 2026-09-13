from app.application.dto.user_dto import IdDTO, UserResponseDTO
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.use_cases.user.create_user_use_case import _to_response
from app.domain.exceptions.user_exceptions import UserNotFoundException


class MeUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, data: IdDTO) -> UserResponseDTO:
        async with self.uow:
            user = await self.uow.users.get(data.id)
            if not user:
                raise UserNotFoundException()
            return _to_response(user)
