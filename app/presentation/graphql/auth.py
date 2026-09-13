from jose import JWTError
from starlette.requests import Request

from app.application.interfaces.token_service import TokenService
from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.entities.user import User
from app.domain.exceptions.user_exceptions import ForbiddenException
from app.domain.value_objects.role import Role
from app.presentation.graphql.context import GraphQLContext
from app.presentation.graphql.errors import raise_graphql_app_exception
from app.utils.app_exception import AppException


async def resolve_user_from_request(
    request: Request,
    uow: UnitOfWork,
    token_service: TokenService,
) -> User | None:
    auth = request.headers.get("Authorization") or request.headers.get("authorization")
    if not auth or not auth.lower().startswith("bearer "):
        return None

    token = auth.split(" ", 1)[1].strip()
    try:
        payload = token_service.verify_access_token(token)
    except JWTError:
        return None

    async with uow:
        user = await uow.users.get(payload.id)
        if not user or not user.active:
            return None
        return user


def require_user(user: User | None, request: Request | None = None) -> User:
    if user is not None:
        return user

    from app.domain.exceptions.auth_exceptions import UserNotAuthorizedException

    exc = UserNotAuthorizedException()
    if request is not None:
        raise_graphql_app_exception(exc, request)
    raise exc


def require_admin(user: User | None, request: Request | None = None) -> User:
    current = require_user(user, request)
    if current.role != Role.ADMIN:
        exc = ForbiddenException()
        if request is not None:
            raise_graphql_app_exception(exc, request)
        raise exc
    return current


async def require_user_ctx(ctx: GraphQLContext) -> User:
    try:
        return require_user(await ctx.get_current_user(), ctx.request)
    except AppException as exc:
        raise_graphql_app_exception(exc, ctx.request)
        raise


async def require_admin_ctx(ctx: GraphQLContext) -> User:
    try:
        return require_admin(await ctx.get_current_user(), ctx.request)
    except AppException as exc:
        raise_graphql_app_exception(exc, ctx.request)
        raise
