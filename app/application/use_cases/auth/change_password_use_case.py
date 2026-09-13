from app.application.dto.auth_dto import ChangePasswordDTO, SuccessDTO
from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.exceptions.user_exceptions import UserNotFoundException
from app.domain.services.password_hasher import PasswordHasher


class ChangePasswordUseCase:
    """Admin changes another user's password."""

    def __init__(self, uow: UnitOfWork, password_hasher: PasswordHasher):
        self.uow = uow
        self.password_hasher = password_hasher

    async def execute(self, data: ChangePasswordDTO) -> SuccessDTO:
        async with self.uow:
            user = await self.uow.users.get(data.user_id)
            if not user:
                raise UserNotFoundException()

            new_hash = self.password_hasher.hash(data.new_password)
            await self.uow.users.update_password(data.user_id, new_hash)
            await self.uow.users.set_refresh_token_hash(data.user_id, None)
            await self.uow.commit()

        return SuccessDTO(success=True)
