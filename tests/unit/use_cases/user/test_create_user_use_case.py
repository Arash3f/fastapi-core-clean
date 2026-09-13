from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.application.dto.user_dto import CreateUserDTO
from app.application.use_cases.user.create_user_use_case import CreateUserUseCase
from app.domain.entities.user import User
from app.domain.exceptions.user_exceptions import UsernameDuplicatedException
from app.domain.value_objects.role import Role


@pytest.mark.asyncio
async def test_create_user_success(mock_uow):
    created = User(
        id=uuid4(),
        username="newuser",
        password_hash="hashed",
        name="New User",
        active=True,
        role=Role.MEMBER,
    )
    mock_uow.users.get_by_username = AsyncMock(return_value=None)
    mock_uow.users.create = AsyncMock(return_value=created)

    hasher = MagicMock()
    hasher.hash.return_value = "hashed"

    result = await CreateUserUseCase(mock_uow, hasher).execute(
        CreateUserDTO(name="New User", username="NewUser", password="pass")
    )

    assert result.username == "newuser"
    assert result.name == "New User"
    mock_uow.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_user_duplicate(mock_uow):
    mock_uow.users.get_by_username = AsyncMock(
        return_value=User(
            id=uuid4(),
            username="newuser",
            password_hash="h",
            name="X",
            active=True,
            role=Role.MEMBER,
        )
    )

    with pytest.raises(UsernameDuplicatedException):
        await CreateUserUseCase(mock_uow, MagicMock()).execute(
            CreateUserDTO(name="X", username="newuser", password="p")
        )
