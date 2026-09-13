import pytest
import pytest_asyncio
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.infrastructure.database.base import Base
from app.infrastructure.services.unit_of_work.sqlalchemy_uow import SQLAlchemyUnitOfWork


@pytest.fixture(scope="module")
def db_engine():
    return create_async_engine(
        settings.database_test_asy,
        echo=False,
        poolclass=NullPool,
    )


@pytest_asyncio.fixture(scope="module", autouse=True, loop_scope="module")
async def prepare_database(db_engine):
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await db_engine.dispose()


@pytest_asyncio.fixture(loop_scope="module")
async def db_connection(db_engine):
    async with db_engine.connect() as connection:
        transaction = await connection.begin()
        try:
            yield connection
        finally:
            await transaction.rollback()


@pytest_asyncio.fixture(loop_scope="module")
async def session_factory(db_connection):
    return async_sessionmaker(
        bind=db_connection,
        class_=AsyncSession,
        expire_on_commit=False,
    )


@pytest_asyncio.fixture(loop_scope="module")
async def uow(session_factory):
    yield SQLAlchemyUnitOfWork(session_factory=session_factory)
