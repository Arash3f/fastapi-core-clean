from app.application.dto.auth_dto import RegisterDTO, TokenResponseDTO
from app.application.dto.auth_dto import LoginDTO
from app.application.interfaces.token_service import TokenService
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.use_cases.auth.login_use_case import LoginUseCase
from app.domain.entities.user import User
from app.domain.exceptions.user_exceptions import UsernameDuplicatedException
from app.domain.services.password_hasher import PasswordHasher
from app.domain.value_objects.role import Role


class RegisterUseCase:
    def __init__(
        self,
        uow: UnitOfWork,
        password_hasher: PasswordHasher,
        token_service: TokenService,
    ):
        self.uow = uow
        self.password_hasher = password_hasher
        self.token_service = token_service

    async def execute(self, data: RegisterDTO) -> TokenResponseDTO:
        username = data.username.lower().strip()

        async with self.uow:
            existing = await self.uow.users.get_by_username(username)
            if existing:
                raise UsernameDuplicatedException()

            user = User(
                username=username,
                password_hash=self.password_hasher.hash(data.password),
                name=data.name.strip(),
                active=True,
                role=Role.MEMBER,
            )
            await self.uow.users.create(user)
            await self.uow.commit()

        login = LoginUseCase(self.uow, self.password_hasher, self.token_service)
        return await login.execute(
            LoginDTO(
                username=username,
                password=data.password,
                device_id=data.device_id,
            )
        )
