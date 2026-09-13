from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.application.interfaces.token_service import TokenService
from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.entities.user import User
from app.domain.exceptions.auth_exceptions import (
    InvalidCredentialsException,
    UserNotAuthorizedException,
)
from app.domain.exceptions.user_exceptions import (
    ForbiddenException,
    UserNotFoundException,
)
from app.domain.value_objects.role import Role
from app.presentation.rest.utils.dependencies import get_token_service, get_uow

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    uow: UnitOfWork = Depends(get_uow),
    token_service: TokenService = Depends(get_token_service),
) -> User:
    try:
        payload = token_service.verify_access_token(token)
    except JWTError:
        raise InvalidCredentialsException()

    async with uow:
        user = await uow.users.get(payload.id)
        if not user:
            raise UserNotFoundException()
        if not user.active:
            raise UserNotAuthorizedException()
        return user


async def require_logged_in(user: User = Depends(get_current_user)) -> User:
    return user


async def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != Role.ADMIN:
        raise ForbiddenException()
    return user


def get_current_user_id(user: User = Depends(require_logged_in)) -> UUID:
    return user.safe_id
