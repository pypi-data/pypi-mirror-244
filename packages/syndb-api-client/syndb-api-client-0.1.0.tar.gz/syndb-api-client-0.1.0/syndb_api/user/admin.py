import contextlib
from logging import getLogger
from uuid import UUID

from fastapi_users import models
from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from syndb_api.database.context import get_db_write_async_session_context
from syndb_api.user.manager import get_user_db, get_user_manager
from syndb_api.user.schema import UserCreate

logger = getLogger(__name__)

get_user_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(email: str, password: str, is_superuser: bool = False, is_verified: bool = False):
    logger.warning(f"Creating superuser: {email}; password: {password}")
    if not (email and password):
        raise ValueError("Both email and password needs to be defined for user creation")

    try:
        async with get_db_write_async_session_context() as session:
            async with get_user_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    await user_manager.create(
                        UserCreate(
                            email=EmailStr(email),
                            password=password,
                            is_superuser=is_superuser,
                            is_verified=is_verified,
                        )
                    )
                    logger.info(f"CreateReadd user with email {email}")
    except UserAlreadyExists:
        logger.error(f'User with email "{email}" already exists')


async def query_user(name: str | None = None, user_id: UUID | None = None):
    if not (name or user_id):
        raise ValueError("Either email or id must be defined for user query")

    async with get_user_user_db_context() as user_db:
        async with get_user_manager_context(user_db) as user_manager:
            if user_id:
                return await user_manager.get(user_id)
            return await user_manager.get_by_email(name)


async def delete_user_by_model(user: models.ID):
    async with get_user_user_db_context() as user_db:
        async with get_user_manager_context(user_db) as user_manager:
            return await user_manager.delete(user)
