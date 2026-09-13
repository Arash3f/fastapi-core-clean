from app.application.dto.auth_dto import SuccessDTO
from app.application.dto.user_dto import IdDTO
from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.exceptions.user_exceptions import UserNotFoundException


class DeleteUserUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, data: IdDTO) -> SuccessDTO:
        async with self.uow:
            user = await self.uow.users.get(data.id)
            if not user:
                raise UserNotFoundException()

            await self.uow.users.soft_delete(data.id)
            await self.uow.users.set_refresh_token_hash(data.id, None)
            await self.uow.commit()

        return SuccessDTO(success=True)
