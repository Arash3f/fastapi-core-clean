import strawberry

from app.application.dto.auth_dto import (
    ChangeMyPasswordDTO,
    ChangePasswordDTO,
    LoginDTO,
    LogoutDTO,
    RefreshTokenDTO,
    RegisterDTO,
)
from app.application.dto.user_dto import (
    CreateUserDTO,
    IdDTO,
    UpdateMeDTO,
    UpdateUserDTO,
)
from app.application.use_cases.auth.change_my_password_use_case import (
    ChangeMyPasswordUseCase,
)
from app.application.use_cases.auth.change_password_use_case import (
    ChangePasswordUseCase,
)
from app.application.use_cases.auth.login_use_case import LoginUseCase
from app.application.use_cases.auth.logout_use_case import LogoutUseCase
from app.application.use_cases.auth.refresh_token_use_case import RefreshTokenUseCase
from app.application.use_cases.auth.register_use_case import RegisterUseCase
from app.application.use_cases.user.create_user_use_case import CreateUserUseCase
from app.application.use_cases.user.delete_user_use_case import DeleteUserUseCase
from app.application.use_cases.user.update_me_use_case import UpdateMeUseCase
from app.application.use_cases.user.update_user_use_case import UpdateUserUseCase
from app.core.throttle import enforce_auth_rate_limit
from app.presentation.graphql.auth import require_admin, require_user
from app.presentation.graphql.context import GraphQLContext
from app.presentation.graphql.mappers.user import user_to_gql
from app.presentation.graphql.types import (
    ChangeMyPasswordInput,
    ChangePasswordInput,
    CreateUserInput,
    LoginInput,
    RefreshTokenInput,
    RegisterInput,
    SuccessType,
    TokenType,
    UpdateMeInput,
    UpdateUserInput,
    UserType,
)


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def login(
        self, info: strawberry.Info[GraphQLContext, None], input: LoginInput
    ) -> TokenType:
        ctx = info.context
        enforce_auth_rate_limit(ctx.request)
        result = await LoginUseCase(
            ctx.uow, ctx.password_hasher, ctx.token_service
        ).execute(
            LoginDTO(
                username=input.username,
                password=input.password,
                device_id=ctx.device_id,
            )
        )
        return TokenType(
            access_token=result.access_token, refresh_token=result.refresh_token
        )

    @strawberry.mutation
    async def register(
        self, info: strawberry.Info[GraphQLContext, None], input: RegisterInput
    ) -> TokenType:
        ctx = info.context
        enforce_auth_rate_limit(ctx.request)
        result = await RegisterUseCase(
            ctx.uow, ctx.password_hasher, ctx.token_service
        ).execute(
            RegisterDTO(
                name=input.name,
                username=input.username,
                password=input.password,
                device_id=ctx.device_id,
            )
        )
        return TokenType(
            access_token=result.access_token, refresh_token=result.refresh_token
        )

    @strawberry.mutation
    async def logout(self, info: strawberry.Info[GraphQLContext, None]) -> SuccessType:
        ctx = info.context
        user = require_user(await ctx.get_current_user(), ctx.request)
        result = await LogoutUseCase(ctx.uow).execute(LogoutDTO(user_id=user.safe_id))
        return SuccessType(success=result.success)

    @strawberry.mutation
    async def refresh_token(
        self, info: strawberry.Info[GraphQLContext, None], input: RefreshTokenInput
    ) -> TokenType:
        ctx = info.context
        enforce_auth_rate_limit(ctx.request)
        result = await RefreshTokenUseCase(
            ctx.uow, ctx.password_hasher, ctx.token_service
        ).execute(
            RefreshTokenDTO(refresh_token=input.refresh_token, device_id=ctx.device_id)
        )
        return TokenType(
            access_token=result.access_token, refresh_token=result.refresh_token
        )

    @strawberry.mutation
    async def change_my_password(
        self, info: strawberry.Info[GraphQLContext, None], input: ChangeMyPasswordInput
    ) -> SuccessType:
        ctx = info.context
        user = require_user(await ctx.get_current_user(), ctx.request)
        result = await ChangeMyPasswordUseCase(ctx.uow, ctx.password_hasher).execute(
            ChangeMyPasswordDTO(
                user_id=user.safe_id,
                current_password=input.current_password,
                new_password=input.new_password,
            )
        )
        return SuccessType(success=result.success)

    @strawberry.mutation
    async def change_password(
        self, info: strawberry.Info[GraphQLContext, None], input: ChangePasswordInput
    ) -> SuccessType:
        ctx = info.context
        require_admin(await ctx.get_current_user(), ctx.request)
        result = await ChangePasswordUseCase(ctx.uow, ctx.password_hasher).execute(
            ChangePasswordDTO(user_id=input.user_id, new_password=input.new_password)
        )
        return SuccessType(success=result.success)

    @strawberry.mutation
    async def create_user(
        self, info: strawberry.Info[GraphQLContext, None], input: CreateUserInput
    ) -> UserType:
        ctx = info.context
        require_admin(await ctx.get_current_user(), ctx.request)
        result = await CreateUserUseCase(ctx.uow, ctx.password_hasher).execute(
            CreateUserDTO(
                name=input.name,
                username=input.username,
                password=input.password,
                role=input.role.to_domain(),
            )
        )
        return user_to_gql(result)

    @strawberry.mutation
    async def update_me(
        self, info: strawberry.Info[GraphQLContext, None], input: UpdateMeInput
    ) -> UserType:
        ctx = info.context
        user = require_user(await ctx.get_current_user(), ctx.request)
        result = await UpdateMeUseCase(ctx.uow).execute(
            UpdateMeDTO(user_id=user.safe_id, name=input.name, username=input.username)
        )
        return user_to_gql(result)

    @strawberry.mutation
    async def update_user(
        self, info: strawberry.Info[GraphQLContext, None], input: UpdateUserInput
    ) -> UserType:
        ctx = info.context
        require_admin(await ctx.get_current_user(), ctx.request)
        result = await UpdateUserUseCase(ctx.uow).execute(
            UpdateUserDTO(
                id=input.id,
                name=input.name,
                username=input.username,
                role=input.role.to_domain() if input.role else None,
                active=input.active,
            )
        )
        return user_to_gql(result)

    @strawberry.mutation
    async def delete_user(
        self, info: strawberry.Info[GraphQLContext, None], user_id: strawberry.ID
    ) -> SuccessType:
        from uuid import UUID

        ctx = info.context
        require_admin(await ctx.get_current_user(), ctx.request)
        result = await DeleteUserUseCase(ctx.uow).execute(IdDTO(id=UUID(str(user_id))))
        return SuccessType(success=result.success)
