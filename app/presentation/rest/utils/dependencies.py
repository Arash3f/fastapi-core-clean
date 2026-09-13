from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.services.password_hasher import PasswordHasher
from app.infrastructure.database.session import async_session
from app.infrastructure.services.security.password_hasher_impl import (
    Argon2PasswordHasher,
)
from app.infrastructure.services.security.token_service_imp import JWTService
from app.infrastructure.services.unit_of_work.sqlalchemy_uow import SQLAlchemyUnitOfWork


def get_uow() -> UnitOfWork:
    return SQLAlchemyUnitOfWork(async_session)


def get_password_hasher() -> PasswordHasher:
    return Argon2PasswordHasher()


def get_token_service() -> JWTService:
    return JWTService()
