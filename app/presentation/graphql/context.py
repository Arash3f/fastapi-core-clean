from strawberry.fastapi import BaseContext

from app.application.interfaces.token_service import TokenService
from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.entities.user import User
from app.domain.services.password_hasher import PasswordHasher
from app.presentation.rest.utils.dependencies import (
    get_password_hasher,
    get_token_service,
    get_uow,
)
from app.presentation.rest.utils.device_fingerprint import get_device_fingerprint


class GraphQLContext(BaseContext):
    def __init__(
        self,
        uow: UnitOfWork,
        token_service: TokenService,
        password_hasher: PasswordHasher,
    ):
        self.uow = uow
        self.token_service = token_service
        self.password_hasher = password_hasher
        self._current_user: User | None = None
        self._current_user_loaded = False

    @property
    def device_id(self) -> str:
        if self.request is None:
            return "unknown"
        return get_device_fingerprint(self.request)

    async def get_current_user(self) -> User | None:
        if self._current_user_loaded:
            return self._current_user

        from app.presentation.graphql.auth import resolve_user_from_request

        if self.request is not None:
            self._current_user = await resolve_user_from_request(
                self.request, self.uow, self.token_service
            )
        self._current_user_loaded = True
        return self._current_user


async def get_graphql_context() -> GraphQLContext:
    return GraphQLContext(
        uow=get_uow(),
        token_service=get_token_service(),
        password_hasher=get_password_hasher(),
    )
