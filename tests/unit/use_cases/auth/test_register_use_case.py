from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from app.application.dto.auth_dto import RegisterDTO
from app.application.interfaces.token_service import TokenPair
from app.application.use_cases.auth.register_use_case import RegisterUseCase
from app.domain.entities.user import User
from app.domain.exceptions.user_exceptions import UsernameDuplicatedException
from app.domain.value_objects.role import Role


@pytest.mark.asyncio
async def test_register_success(mock_uow):
    mock_uow.users.get_by_username = AsyncMock(
        side_effect=[
            None,
            User(
                id=uuid4(),
                username="member",
                password_hash="hashed",
                name="Member",
                active=True,
                role=Role.MEMBER,
            ),
        ]
    )
    mock_uow.users.create = AsyncMock(
        return_value=User(
            id=uuid4(),
            username="member",
            password_hash="hashed",
            name="Member",
            active=True,
            role=Role.MEMBER,
        )
    )

    password_hasher = MagicMock()
    password_hasher.hash.return_value = "hashed"
    password_hasher.verify.return_value = True

    token_service = MagicMock()
    token_service.sign_token_pair.return_value = TokenPair(
        access_token="a", refresh_token="r"
    )

    result = await RegisterUseCase(mock_uow, password_hasher, token_service).execute(
        RegisterDTO(name="Member", username="Member", password="pass", device_id="dev")
    )

    assert result.access_token == "a"
    mock_uow.users.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_register_duplicate_username(mock_uow):
    mock_uow.users.get_by_username = AsyncMock(
        return_value=User(
            id=uuid4(),
            username="member",
            password_hash="h",
            name="M",
            active=True,
            role=Role.MEMBER,
        )
    )

    with pytest.raises(UsernameDuplicatedException):
        await RegisterUseCase(mock_uow, MagicMock(), MagicMock()).execute(
            RegisterDTO(name="M", username="member", password="p", device_id="d")
        )
