from jose import JWTError

from app.application.dto.auth_dto import RefreshTokenDTO, TokenResponseDTO
from app.application.interfaces.token_service import TokenService
from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.exceptions.auth_exceptions import (
    DeviceMismatchException,
    InvalidRefreshTokenException,
    UserNotAuthorizedException,
)
from app.domain.services.password_hasher import PasswordHasher


class RefreshTokenUseCase:
    def __init__(
        self,
        uow: UnitOfWork,
        password_hasher: PasswordHasher,
        token_service: TokenService,
    ):
        self.uow = uow
        self.password_hasher = password_hasher
        self.token_service = token_service

    async def execute(self, data: RefreshTokenDTO) -> TokenResponseDTO:
        try:
            payload = self.token_service.verify_refresh_token(data.refresh_token)
        except JWTError:
            raise InvalidRefreshTokenException()

        if payload.device_id != data.device_id:
            raise DeviceMismatchException()

        async with self.uow:
            user = await self.uow.users.get(payload.id)
            if not user or not user.active or not user.refresh_token_hash:
                raise UserNotAuthorizedException()

            if not self.password_hasher.verify(
                data.refresh_token, user.refresh_token_hash
            ):
                raise InvalidRefreshTokenException()

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
