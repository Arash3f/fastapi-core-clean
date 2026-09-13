from unittest.mock import AsyncMock, MagicMock

import pytest

from app.application.interfaces.unit_of_work import UnitOfWork
from app.domain.repositories.user_repository import UserRepository


@pytest.fixture
def mock_uow():
    users_repo = MagicMock(spec_set=UserRepository)
    users_repo.create = AsyncMock()
    users_repo.get = AsyncMock()
    users_repo.get_by_username = AsyncMock()
    users_repo.get_or_raise = AsyncMock()
    users_repo.update = AsyncMock()
    users_repo.soft_delete = AsyncMock()
    users_repo.set_refresh_token_hash = AsyncMock()
    users_repo.update_password = AsyncMock()
    users_repo.get_list_by_filter = AsyncMock()

    uow = MagicMock(spec=UnitOfWork)
    uow.users = users_repo
    uow.__aenter__ = AsyncMock(return_value=uow)
    uow.__aexit__ = AsyncMock(return_value=None)
    uow.commit = AsyncMock()
    uow.rollback = AsyncMock()
    return uow
