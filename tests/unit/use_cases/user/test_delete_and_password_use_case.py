from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.application.dto.auth_dto import ChangeMyPasswordDTO
from app.application.dto.user_dto import IdDTO
from app.application.use_cases.auth.change_my_password_use_case import (
    ChangeMyPasswordUseCase,
)
from app.application.use_cases.user.delete_user_use_case import DeleteUserUseCase
from app.domain.entities.user import User
from app.domain.exceptions.auth_exceptions import IncorrectCurrentPasswordException
from app.domain.exceptions.user_exceptions import UserNotFoundException
from app.domain.value_objects.role import Role


@pytest.mark.asyncio
async def test_change_my_password_success(mock_uow):
    user = User(
        id=uuid4(),
        username="admin",
        password_hash="old-hash",
        name="Admin",
        active=True,
        role=Role.ADMIN,
    )
    mock_uow.users.get = AsyncMock(return_value=user)
    password_hasher = MagicMock()
    password_hasher.verify.return_value = True
    password_hasher.hash.return_value = "new-hash"

    result = await ChangeMyPasswordUseCase(mock_uow, password_hasher).execute(
        ChangeMyPasswordDTO(
            user_id=user.safe_id,
            current_password="old",
            new_password="new-password-123",
        )
    )

    assert result.success is True
    mock_uow.users.update_password.assert_awaited_once_with(user.safe_id, "new-hash")
    mock_uow.users.set_refresh_token_hash.assert_awaited_once_with(user.safe_id, None)


@pytest.mark.asyncio
async def test_change_my_password_wrong_current(mock_uow):
    user = User(
        id=uuid4(),
        username="admin",
        password_hash="old-hash",
        name="Admin",
        active=True,
        role=Role.ADMIN,
    )
    mock_uow.users.get = AsyncMock(return_value=user)
    password_hasher = MagicMock()
    password_hasher.verify.return_value = False

    with pytest.raises(IncorrectCurrentPasswordException):
        await ChangeMyPasswordUseCase(mock_uow, password_hasher).execute(
            ChangeMyPasswordDTO(
                user_id=user.safe_id,
                current_password="wrong",
                new_password="new-password-123",
            )
        )


@pytest.mark.asyncio
async def test_delete_user_success(mock_uow):
    user = User(
        id=uuid4(),
        username="member",
        password_hash="hash",
        name="Member",
        active=True,
        role=Role.MEMBER,
    )
    mock_uow.users.get = AsyncMock(return_value=user)

    result = await DeleteUserUseCase(mock_uow).execute(IdDTO(id=user.safe_id))

    assert result.success is True
    mock_uow.users.soft_delete.assert_awaited_once_with(user.safe_id)
    mock_uow.users.set_refresh_token_hash.assert_awaited_once_with(user.safe_id, None)


@pytest.mark.asyncio
async def test_delete_user_not_found(mock_uow):
    mock_uow.users.get = AsyncMock(return_value=None)

    with pytest.raises(UserNotFoundException):
        await DeleteUserUseCase(mock_uow).execute(IdDTO(id=uuid4()))
