from app.application.dto.auth_dto import LoginDTO, TokenResponseDTO
from app.application.interfaces.token_service import TokenService
from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.exceptions.auth_exceptions import (
    InactiveUserException,
    InvalidCredentialsException,
)
from app.domain.services.password_hasher import PasswordHasher


class LoginUseCase:
    def __init__(
        self,
        uow: UnitOfWork,
        password_hasher: PasswordHasher,
        token_service: TokenService,
    ):
        self.uow = uow
        self.password_hasher = password_hasher
        self.token_service = token_service

    async def execute(self, data: LoginDTO) -> TokenResponseDTO:
        username = data.username.lower().strip()

        async with self.uow:
            user = await self.uow.users.get_by_username(username)
            if not user:
                raise InvalidCredentialsException()

            if not user.active:
                raise InactiveUserException()

            if not self.password_hasher.verify(data.password, user.password_hash):
                raise InvalidCredentialsException()

            tokens = self.token_service.sign_token_pair(
                user_id=user.safe_id,
                username=user.username,
                device_id=data.device_id,
                role=user.role,
            )

            refresh_hash = self.password_hasher.hash(tokens.refresh_token)
            await self.uow.users.set_refresh_token_hash(user.safe_id, refresh_hash)
            await self.uow.commit()

            return TokenResponseDTO(
                access_token=tokens.access_token,
                refresh_token=tokens.refresh_token,
            )
