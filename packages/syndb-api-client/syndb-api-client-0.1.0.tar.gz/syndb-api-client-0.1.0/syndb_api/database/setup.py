import time
from functools import cached_property
from typing import AsyncGenerator
from uuid import UUID

import asyncpg
from fastapi import Request
from fastapi_users.exceptions import UserAlreadyExists
from pydantic import BaseModel, computed_field
from scyllapy import Scylla
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from syndb_constants.api import TEST_PASSWORD, TEST_USERNAME

from syndb_api.database.base_model import Base
from syndb_api.neurodata.metadata.dataset.workflow import id_to_label
from syndb_api.neurodata.model import Dataset
from syndb_api.settings.constant import cluster_settings, settings
from syndb_api.user.model import User
from syndb_api.user.schema import UserCreate


def create_db_async_session_maker(engine: AsyncEngine):
    return async_sessionmaker(engine, expire_on_commit=False)


async def get_cluster_db_write_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with create_db_async_session_maker(cluster_settings.db_write_engine())() as session:
        yield session


async def get_db_write_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with create_db_async_session_maker(settings.db_write_engine())() as session:
        yield session


async def get_db_read_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with create_db_async_session_maker(settings.db_read_engine())() as session:
        yield session


async def get_scylla_session(request: Request) -> Scylla:
    return request.app.state.scylla


class DataInDB(BaseModel, arbitrary_types_allowed=True):
    user: User
    dataset_a: Dataset
    dataset_b: Dataset
    dataset_c: Dataset

    @computed_field  # type: ignore[misc]
    @cached_property
    def datasets_id_to_label(self) -> dict[UUID, str]:
        return id_to_label([self.dataset_a, self.dataset_b, self.dataset_c])

    @computed_field  # type: ignore[misc]
    @cached_property
    def dataset_a_id_to_label(self) -> dict[UUID, str]:
        return id_to_label([self.dataset_a, self.dataset_b, self.dataset_c])

    @computed_field  # type: ignore[misc]
    @cached_property
    def dataset_b_id_to_label(self) -> dict[UUID, str]:
        return id_to_label([self.dataset_a, self.dataset_b, self.dataset_c])

    @computed_field  # type: ignore[misc]
    @cached_property
    def dataset_c_id_to_label(self) -> dict[UUID, str]:
        return id_to_label([self.dataset_a, self.dataset_b, self.dataset_c])


async def setup_postgres() -> DataInDB:
    from syndb_api.database.mock import register_mock_datasets
    from syndb_api.database.pre_defined import pre_animal_objects
    from syndb_api.user.admin import get_user_manager_context, get_user_user_db_context

    max_retries = 30
    while True:
        try:
            await asyncpg.connect(
                user=settings.postgres_username,
                password=settings.postgres_password,
                host=settings.postgres_host,
                port=settings.postgres_port,
                database=settings.postgres_path,
            )
            break
        except (ConnectionResetError, ConnectionError) as e:
            if not max_retries:
                raise e
            time.sleep(0.5)
            max_retries -= 1

    async with settings.db_write_engine().begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with create_db_async_session_maker(settings.db_write_engine())() as session:
        async with get_user_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                try:
                    user = await user_manager.create(
                        UserCreate(
                            email=TEST_USERNAME,
                            password=TEST_PASSWORD,
                            is_superuser=True,
                            is_verified=True,
                        )
                    )
                except UserAlreadyExists:
                    pass

        session.add_all(list(pre_animal_objects()))
        await session.commit()

        datasets = await register_mock_datasets(session, user)

    return DataInDB(user=user, dataset_a=datasets[0], dataset_b=datasets[1], dataset_c=datasets[2])
