from app.application.dto.user_dto import UserListResponseDTO, UserResponseDTO
from app.presentation.graphql.types import RoleGql, UserListType, UserType


def user_to_gql(dto: UserResponseDTO) -> UserType:
    return UserType(
        id=dto.id,
        username=dto.username,
        name=dto.name,
        active=dto.active,
        role=RoleGql.from_domain(dto.role),
        created_at=dto.created_at,
        updated_at=dto.updated_at,
    )


def user_list_to_gql(dto: UserListResponseDTO) -> UserListType:
    return UserListType(
        items=[user_to_gql(i) for i in dto.items],
        total=dto.total,
        page=dto.page,
        page_size=dto.page_size,
    )
