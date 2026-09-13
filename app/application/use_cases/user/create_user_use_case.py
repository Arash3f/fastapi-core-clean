from app.application.dto.user_dto import CreateUserDTO, UserResponseDTO
from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.entities.user import User
from app.domain.exceptions.user_exceptions import UsernameDuplicatedException
from app.domain.services.password_hasher import PasswordHasher


def _to_response(user: User) -> UserResponseDTO:
    return UserResponseDTO(
        id=user.safe_id,
        username=user.username,
        name=user.name,
        active=user.active,
        role=user.role,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


class CreateUserUseCase:
    def __init__(self, uow: UnitOfWork, password_hasher: PasswordHasher):
        self.uow = uow
        self.password_hasher = password_hasher

    async def execute(self, data: CreateUserDTO) -> UserResponseDTO:
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
                role=data.role,
            )
            created = await self.uow.users.create(user)
            await self.uow.commit()
            return _to_response(created)
