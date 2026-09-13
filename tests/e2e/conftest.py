import pytest
from httpx import ASGITransport, AsyncClient

from app.infrastructure.database.base import Base
from app.infrastructure.database.seed import seed_initial_users
from app.infrastructure.database.session import engine
from app.infrastructure.services.security.password_hasher_impl import (
    Argon2PasswordHasher,
)
from app.main import app
from app.presentation.rest.utils.dependencies import get_uow


@pytest.fixture(scope="module", autouse=True)
async def prepare_e2e_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_initial_users(uow=get_uow(), password_hasher=Argon2PasswordHasher())
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
