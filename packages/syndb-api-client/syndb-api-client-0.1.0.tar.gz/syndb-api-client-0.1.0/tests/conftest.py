import asyncio
from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from syndb_api.database.setup import create_db_async_session_maker, setup_postgres
from syndb_api.settings.constant import settings


@pytest.fixture(scope="session")
def event_loop():
    """Force the pytest-asyncio loop to be the main one."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_test_postgres():
    yield await setup_postgres()


@pytest.fixture
async def sqlalchemy_session(request) -> AsyncGenerator[AsyncSession, None]:
    async with create_db_async_session_maker(settings.db_write_engine())() as session:
        yield session
