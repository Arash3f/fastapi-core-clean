from app.application.dto.auth_dto import LogoutDTO, SuccessDTO
from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.exceptions.user_exceptions import UserNotFoundException


class LogoutUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def execute(self, data: LogoutDTO) -> SuccessDTO:
        async with self.uow:
            user = await self.uow.users.get(data.user_id)
            if not user:
                raise UserNotFoundException()

            await self.uow.users.set_refresh_token_hash(data.user_id, None)
            await self.uow.commit()

        return SuccessDTO(success=True)
