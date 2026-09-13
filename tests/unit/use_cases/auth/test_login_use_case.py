from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.application.dto.auth_dto import LoginDTO
from app.application.use_cases.auth.login_use_case import LoginUseCase
from app.domain.entities.user import User
from app.domain.exceptions.auth_exceptions import (
    InactiveUserException,
    InvalidCredentialsException,
)
from app.domain.value_objects.role import Role
from app.application.interfaces.token_service import TokenPair


@pytest.mark.asyncio
async def test_login_success(mock_uow):
    user = User(
        id=uuid4(),
        username="admin",
        password_hash="hashed",
        name="Admin",
        active=True,
        role=Role.ADMIN,
    )
    mock_uow.users.get_by_username = AsyncMock(return_value=user)

    password_hasher = MagicMock()
    password_hasher.verify.return_value = True
    password_hasher.hash.return_value = "refresh-hash"

    token_service = MagicMock()
    token_service.sign_token_pair.return_value = TokenPair(
        access_token="access", refresh_token="refresh"
    )

    result = await LoginUseCase(mock_uow, password_hasher, token_service).execute(
        LoginDTO(username="Admin", password="secret", device_id="device")
    )

    assert result.access_token == "access"
    assert result.refresh_token == "refresh"
    mock_uow.users.get_by_username.assert_awaited_once_with("admin")
    mock_uow.users.set_refresh_token_hash.assert_awaited_once()
    mock_uow.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_login_invalid_username(mock_uow):
    mock_uow.users.get_by_username = AsyncMock(return_value=None)
    password_hasher = MagicMock()
    token_service = MagicMock()

    with pytest.raises(InvalidCredentialsException):
        await LoginUseCase(mock_uow, password_hasher, token_service).execute(
            LoginDTO(username="x", password="y", device_id="d")
        )


@pytest.mark.asyncio
async def test_login_inactive_user(mock_uow):
    user = User(
        id=uuid4(),
        username="admin",
        password_hash="hashed",
        name="Admin",
        active=False,
        role=Role.ADMIN,
    )
    mock_uow.users.get_by_username = AsyncMock(return_value=user)

    with pytest.raises(InactiveUserException):
        await LoginUseCase(mock_uow, MagicMock(), MagicMock()).execute(
            LoginDTO(username="admin", password="y", device_id="d")
        )


@pytest.mark.asyncio
async def test_login_invalid_password(mock_uow):
    user = User(
        id=uuid4(),
        username="admin",
        password_hash="hashed",
        name="Admin",
        active=True,
        role=Role.ADMIN,
    )
    mock_uow.users.get_by_username = AsyncMock(return_value=user)
    password_hasher = MagicMock()
    password_hasher.verify.return_value = False

    with pytest.raises(InvalidCredentialsException):
        await LoginUseCase(mock_uow, password_hasher, MagicMock()).execute(
            LoginDTO(username="admin", password="wrong", device_id="d")
        )
