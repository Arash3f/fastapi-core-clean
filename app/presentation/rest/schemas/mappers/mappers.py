from app.application.dto.auth_dto import TokenResponseDTO
from app.application.dto.user_dto import UserListResponseDTO, UserResponseDTO
from app.domain.shared.dto.pagination_dto import PaginationParams
from app.domain.shared.dto.sorter_dto import SortParams
from app.domain.shared.dto.user_filter_dto import FilterUserQuery, UserFilters
from app.presentation.rest.schemas.dto.schemas import (
    ReadUsersRequest,
    ReadUsersResponse,
    TokenResponse,
    UserModel,
)


class AuthApiMapper:
    @staticmethod
    def from_token_dto(dto: TokenResponseDTO) -> TokenResponse:
        return TokenResponse(
            access_token=dto.access_token,
            refresh_token=dto.refresh_token,
        )


class UserApiMapper:
    @staticmethod
    def from_user_dto(dto: UserResponseDTO) -> UserModel:
        return UserModel(
            id=dto.id,
            username=dto.username,
            name=dto.name,
            active=dto.active,
            role=dto.role,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )

    @staticmethod
    def to_filter_query(data: ReadUsersRequest) -> FilterUserQuery:
        filters = None
        if data.filters:
            filters = UserFilters(
                id=data.filters.id,
                username=data.filters.username,
                name=data.filters.name,
                role=data.filters.role,
                active=data.filters.active,
            )
        return FilterUserQuery(
            filters=filters,
            pagination=PaginationParams(page=data.page, page_size=data.page_size),
            sort=SortParams(sort_by=data.sort_by, sort_order=data.sort_order),
        )

    @staticmethod
    def from_list_dto(dto: UserListResponseDTO) -> ReadUsersResponse:
        return ReadUsersResponse(
            items=[UserApiMapper.from_user_dto(i) for i in dto.items],
            total=dto.total,
            page=dto.page,
            page_size=dto.page_size,
        )
