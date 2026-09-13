from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.application.dto.auth_dto import (
    ChangeMyPasswordDTO,
    ChangePasswordDTO,
    LoginDTO,
    LogoutDTO,
    RefreshTokenDTO,
    RegisterDTO,
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
from app.core.config import settings
from app.core.throttle import limiter
from app.domain.entities.user import User
from app.presentation.rest.dependencies.auth_dependencies import (
    get_current_user_id,
    require_admin,
    require_logged_in,
)
from app.presentation.rest.schemas.dto.schemas import (
    ChangeMyPasswordRequest,
    ChangePasswordRequest,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    SuccessResponse,
    TokenResponse,
)
from app.presentation.rest.schemas.mappers.mappers import AuthApiMapper
from app.presentation.rest.utils.dependencies import (
    get_password_hasher,
    get_token_service,
    get_uow,
)
from app.presentation.rest.utils.device_fingerprint import get_device_fingerprint

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
@limiter.limit(settings.auth_rate_limit)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    device_id: str = Depends(get_device_fingerprint),
    uow=Depends(get_uow),
    token_service=Depends(get_token_service),
    password_hasher=Depends(get_password_hasher),
) -> TokenResponse:
    usecase = LoginUseCase(uow, password_hasher, token_service)
    result = await usecase.execute(
        LoginDTO(
            username=form_data.username,
            password=form_data.password,
            device_id=device_id,
        )
    )
    return AuthApiMapper.from_token_dto(result)


@router.post("/logIn", response_model=TokenResponse, include_in_schema=False)
@limiter.limit(settings.auth_rate_limit)
async def login_json(
    request: Request,
    data: LoginRequest,
    device_id: str = Depends(get_device_fingerprint),
    uow=Depends(get_uow),
    token_service=Depends(get_token_service),
    password_hasher=Depends(get_password_hasher),
) -> TokenResponse:
    """JSON login (nestJs-core-clean compatible path)."""
    usecase = LoginUseCase(uow, password_hasher, token_service)
    result = await usecase.execute(
        LoginDTO(
            username=data.username,
            password=data.password,
            device_id=device_id,
        )
    )
    return AuthApiMapper.from_token_dto(result)


@router.post("/register", response_model=TokenResponse, status_code=201)
@limiter.limit(settings.auth_rate_limit)
async def register(
    request: Request,
    data: RegisterRequest,
    device_id: str = Depends(get_device_fingerprint),
    uow=Depends(get_uow),
    token_service=Depends(get_token_service),
    password_hasher=Depends(get_password_hasher),
) -> TokenResponse:
    usecase = RegisterUseCase(uow, password_hasher, token_service)
    result = await usecase.execute(
        RegisterDTO(
            name=data.name,
            username=data.username,
            password=data.password,
            device_id=device_id,
        )
    )
    return AuthApiMapper.from_token_dto(result)


@router.post("/logout", response_model=SuccessResponse)
async def logout(
    user_id=Depends(get_current_user_id),
    uow=Depends(get_uow),
    _user: User = Depends(require_logged_in),
) -> SuccessResponse:
    usecase = LogoutUseCase(uow)
    result = await usecase.execute(LogoutDTO(user_id=user_id))
    return SuccessResponse(success=result.success)


@router.post("/refresh", response_model=TokenResponse)
@router.post("/refreshToken", response_model=TokenResponse, include_in_schema=False)
@limiter.limit(settings.auth_rate_limit)
async def refresh_token(
    request: Request,
    data: RefreshTokenRequest,
    device_id: str = Depends(get_device_fingerprint),
    uow=Depends(get_uow),
    token_service=Depends(get_token_service),
    password_hasher=Depends(get_password_hasher),
) -> TokenResponse:
    usecase = RefreshTokenUseCase(uow, password_hasher, token_service)
    result = await usecase.execute(
        RefreshTokenDTO(refresh_token=data.refresh_token, device_id=device_id)
    )
    return AuthApiMapper.from_token_dto(result)


@router.patch("/changeMyPassword", response_model=SuccessResponse)
async def change_my_password(
    data: ChangeMyPasswordRequest,
    user_id=Depends(get_current_user_id),
    uow=Depends(get_uow),
    password_hasher=Depends(get_password_hasher),
    _user: User = Depends(require_logged_in),
) -> SuccessResponse:
    usecase = ChangeMyPasswordUseCase(uow, password_hasher)
    result = await usecase.execute(
        ChangeMyPasswordDTO(
            user_id=user_id,
            current_password=data.current_password,
            new_password=data.new_password,
        )
    )
    return SuccessResponse(success=result.success)


@router.patch("/changePassword", response_model=SuccessResponse)
async def change_password(
    data: ChangePasswordRequest,
    uow=Depends(get_uow),
    password_hasher=Depends(get_password_hasher),
    _admin: User = Depends(require_admin),
) -> SuccessResponse:
    usecase = ChangePasswordUseCase(uow, password_hasher)
    result = await usecase.execute(
        ChangePasswordDTO(user_id=data.user_id, new_password=data.new_password)
    )
    return SuccessResponse(success=result.success)
