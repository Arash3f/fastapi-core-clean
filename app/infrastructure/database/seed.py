from app.application.interfaces.unit_of_work import UnitOfWork
from app.core.config import settings
from app.domain.entities.user import User
from app.domain.value_objects.role import Role
from app.infrastructure.services.security.password_hasher_impl import (
    Argon2PasswordHasher,
)


async def seed_initial_users(uow: UnitOfWork, password_hasher: Argon2PasswordHasher):
    if not settings.SEED_ON_BOOT:
        return

    async with uow:
        await _ensure_user(
            uow,
            password_hasher,
            name=settings.SUPER_USER_NAME,
            username=settings.SUPER_USER_USERNAME,
            password=settings.SUPER_USER_PASSWORD,
            role=Role.ADMIN,
        )

        if (
            settings.MEMBER_USER_USERNAME
            and settings.MEMBER_USER_PASSWORD
            and settings.MEMBER_USER_NAME
        ):
            await _ensure_user(
                uow,
                password_hasher,
                name=settings.MEMBER_USER_NAME,
                username=settings.MEMBER_USER_USERNAME,
                password=settings.MEMBER_USER_PASSWORD,
                role=Role.MEMBER,
            )

        await uow.commit()


async def _ensure_user(
    uow: UnitOfWork,
    password_hasher: Argon2PasswordHasher,
    *,
    name: str,
    username: str,
    password: str,
    role: Role,
) -> None:
    """Create the user only when missing — never overwrite password/role on boot."""
    username = username.lower().strip()
    existing = await uow.users.get_by_username(username)
    if existing:
        return

    await uow.users.create(
        User(
            username=username,
            password_hash=password_hasher.hash(password),
            name=name,
            active=True,
            role=role,
        )
    )
