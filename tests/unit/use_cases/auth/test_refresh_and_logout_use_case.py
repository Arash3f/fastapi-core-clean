from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from jose import JWTError

from app.application.dto.auth_dto import LogoutDTO, RefreshTokenDTO
from app.application.interfaces.token_service import TokenPair, TokenPayload
from app.application.use_cases.auth.logout_use_case import LogoutUseCase
from app.application.use_cases.auth.refresh_token_use_case import RefreshTokenUseCase
from app.domain.entities.user import User
from app.domain.exceptions.auth_exceptions import (
    DeviceMismatchException,
    InvalidRefreshTokenException,
)
from app.domain.exceptions.user_exceptions import UserNotFoundException
from app.domain.value_objects.role import Role


def _user(**kwargs) -> User:
    defaults = dict(
        id=uuid4(),
        username="admin",
        password_hash="hashed",
        name="Admin",
        active=True,
        role=Role.ADMIN,
        refresh_token_hash="stored-hash",
    )
    defaults.update(kwargs)
    return User(**defaults)


@pytest.mark.asyncio
async def test_refresh_success(mock_uow):
    user = _user()
    mock_uow.users.get = AsyncMock(return_value=user)

    password_hasher = MagicMock()
    password_hasher.verify.return_value = True
    password_hasher.hash.return_value = "new-hash"

    token_service = MagicMock()
    token_service.verify_refresh_token.return_value = TokenPayload(
        id=user.safe_id, username=user.username, device_id="device-a", role=user.role
    )
    token_service.sign_token_pair.return_value = TokenPair(
        access_token="access2", refresh_token="refresh2"
    )

    result = await RefreshTokenUseCase(
        mock_uow, password_hasher, token_service
    ).execute(RefreshTokenDTO(refresh_token="refresh1", device_id="device-a"))

    assert result.access_token == "access2"
    assert result.refresh_token == "refresh2"
    mock_uow.users.set_refresh_token_hash.assert_awaited_once()
    mock_uow.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_refresh_device_mismatch(mock_uow):
    user = _user()
    token_service = MagicMock()
    token_service.verify_refresh_token.return_value = TokenPayload(
        id=user.safe_id, username=user.username, device_id="device-a", role=user.role
    )

    with pytest.raises(DeviceMismatchException):
        await RefreshTokenUseCase(mock_uow, MagicMock(), token_service).execute(
            RefreshTokenDTO(refresh_token="refresh1", device_id="device-b")
        )


@pytest.mark.asyncio
async def test_refresh_invalid_jwt(mock_uow):
    token_service = MagicMock()
    token_service.verify_refresh_token.side_effect = JWTError("bad")

    with pytest.raises(InvalidRefreshTokenException):
        await RefreshTokenUseCase(mock_uow, MagicMock(), token_service).execute(
            RefreshTokenDTO(refresh_token="bad", device_id="device-a")
        )


@pytest.mark.asyncio
async def test_logout_success(mock_uow):
    user = _user()
    mock_uow.users.get = AsyncMock(return_value=user)

    result = await LogoutUseCase(mock_uow).execute(LogoutDTO(user_id=user.safe_id))

    assert result.success is True
    mock_uow.users.set_refresh_token_hash.assert_awaited_once_with(user.safe_id, None)
    mock_uow.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_logout_user_not_found(mock_uow):
    mock_uow.users.get = AsyncMock(return_value=None)

    with pytest.raises(UserNotFoundException):
        await LogoutUseCase(mock_uow).execute(LogoutDTO(user_id=uuid4()))
