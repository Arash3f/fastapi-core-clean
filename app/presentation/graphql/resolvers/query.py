import strawberry

from app.application.dto.user_dto import IdDTO
from app.application.use_cases.user.me_use_case import MeUseCase
from app.application.use_cases.user.read_users_with_filter_use_case import (
    ReadUsersWithFilterUseCase,
)
from app.domain.shared.dto.pagination_dto import PaginationParams
from app.domain.shared.dto.sorter_dto import SortOrderField, SortParams
from app.domain.shared.dto.user_filter_dto import (
    FilterUserQuery,
    UserFilters,
    UserSortField,
)
from app.presentation.graphql.auth import require_admin, require_user
from app.presentation.graphql.context import GraphQLContext
from app.presentation.graphql.mappers.user import user_list_to_gql, user_to_gql
from app.presentation.graphql.types import ReadUsersInput, UserListType, UserType


@strawberry.type
class Query:
    @strawberry.field
    async def me(self, info: strawberry.Info[GraphQLContext, None]) -> UserType:
        ctx = info.context
        user = require_user(await ctx.get_current_user(), ctx.request)
        result = await MeUseCase(ctx.uow).execute(IdDTO(id=user.safe_id))
        return user_to_gql(result)

    @strawberry.field
    async def users(
        self,
        info: strawberry.Info[GraphQLContext, None],
        input: ReadUsersInput | None = None,
    ) -> UserListType:
        ctx = info.context
        require_admin(await ctx.get_current_user(), ctx.request)
        data = input or ReadUsersInput()
        filters = None
        if data.filters:
            filters = UserFilters(
                username=data.filters.username,
                name=data.filters.name,
                role=data.filters.role.to_domain() if data.filters.role else None,
                active=data.filters.active,
            )
        query = FilterUserQuery(
            filters=filters,
            pagination=PaginationParams(page=data.page, page_size=data.page_size),
            sort=SortParams(
                sort_by=UserSortField.CREATED_AT, sort_order=SortOrderField.DESC
            ),
        )
        result = await ReadUsersWithFilterUseCase(ctx.uow).execute(query)
        return user_list_to_gql(result)
