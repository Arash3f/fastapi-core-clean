from uuid import UUID

from fastapi import APIRouter, Depends

from app.application.dto.user_dto import (
    CreateUserDTO,
    IdDTO,
    UpdateMeDTO,
    UpdateUserDTO,
)
from app.application.use_cases.user.create_user_use_case import CreateUserUseCase
from app.application.use_cases.user.delete_user_use_case import DeleteUserUseCase
from app.application.use_cases.user.me_use_case import MeUseCase
from app.application.use_cases.user.read_users_with_filter_use_case import (
    ReadUsersWithFilterUseCase,
)
from app.application.use_cases.user.update_me_use_case import UpdateMeUseCase
from app.application.use_cases.user.update_user_use_case import UpdateUserUseCase
from app.domain.entities.user import User
from app.presentation.rest.dependencies.auth_dependencies import (
    get_current_user_id,
    require_admin,
    require_logged_in,
)
from app.presentation.rest.schemas.dto.schemas import (
    CreateUserRequest,
    ReadUsersRequest,
    ReadUsersResponse,
    SuccessResponse,
    UpdateMeRequest,
    UpdateUserRequest,
    UserModel,
)
from app.presentation.rest.schemas.mappers.mappers import UserApiMapper
from app.presentation.rest.utils.dependencies import get_password_hasher, get_uow

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/me", response_model=UserModel)
async def me(
    user_id: UUID = Depends(get_current_user_id),
    uow=Depends(get_uow),
    _user: User = Depends(require_logged_in),
) -> UserModel:
    result = await MeUseCase(uow).execute(IdDTO(id=user_id))
    return UserApiMapper.from_user_dto(result)


@router.post("/updateMe", response_model=UserModel)
async def update_me(
    data: UpdateMeRequest,
    user_id: UUID = Depends(get_current_user_id),
    uow=Depends(get_uow),
    _user: User = Depends(require_logged_in),
) -> UserModel:
    result = await UpdateMeUseCase(uow).execute(
        UpdateMeDTO(user_id=user_id, name=data.name, username=data.username)
    )
    return UserApiMapper.from_user_dto(result)


@router.post("/createUser", response_model=UserModel, status_code=201)
async def create_user(
    data: CreateUserRequest,
    uow=Depends(get_uow),
    password_hasher=Depends(get_password_hasher),
    _admin: User = Depends(require_admin),
) -> UserModel:
    result = await CreateUserUseCase(uow, password_hasher).execute(
        CreateUserDTO(
            name=data.name,
            username=data.username,
            password=data.password,
            role=data.role,
        )
    )
    return UserApiMapper.from_user_dto(result)


@router.get("", response_model=ReadUsersResponse)
async def read_users(
    page: int = 1,
    page_size: int = 20,
    username: str | None = None,
    name: str | None = None,
    active: bool | None = None,
    uow=Depends(get_uow),
    _admin: User = Depends(require_admin),
) -> ReadUsersResponse:
    from app.presentation.rest.schemas.dto.schemas import UserFiltersRequest

    filters = None
    if any(v is not None for v in (username, name, active)):
        filters = UserFiltersRequest(username=username, name=name, active=active)

    request = ReadUsersRequest(page=page, page_size=page_size, filters=filters)
    result = await ReadUsersWithFilterUseCase(uow).execute(
        UserApiMapper.to_filter_query(request)
    )
    return UserApiMapper.from_list_dto(result)


@router.post("/list", response_model=ReadUsersResponse)
async def read_users_with_body(
    data: ReadUsersRequest,
    uow=Depends(get_uow),
    _admin: User = Depends(require_admin),
) -> ReadUsersResponse:
    result = await ReadUsersWithFilterUseCase(uow).execute(
        UserApiMapper.to_filter_query(data)
    )
    return UserApiMapper.from_list_dto(result)


@router.post("/updateUser", response_model=UserModel)
async def update_user(
    data: UpdateUserRequest,
    uow=Depends(get_uow),
    _admin: User = Depends(require_admin),
) -> UserModel:
    result = await UpdateUserUseCase(uow).execute(
        UpdateUserDTO(
            id=data.id,
            name=data.name,
            username=data.username,
            role=data.role,
            active=data.active,
        )
    )
    return UserApiMapper.from_user_dto(result)


@router.delete("/{user_id}", response_model=SuccessResponse)
async def delete_user(
    user_id: UUID,
    uow=Depends(get_uow),
    _admin: User = Depends(require_admin),
) -> SuccessResponse:
    result = await DeleteUserUseCase(uow).execute(IdDTO(id=user_id))
    return SuccessResponse(success=result.success)
