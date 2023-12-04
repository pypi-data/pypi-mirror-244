from logging import getLogger
from typing import AsyncGenerator, Optional
from uuid import UUID

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import AuthenticationBackend, BearerTransport
from fastapi_users.authentication.strategy import AccessTokenDatabase, DatabaseStrategy
from fastapi_users.password import PasswordHelper
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from syndb_api.database.setup import get_db_write_async_session
from syndb_api.settings.constant import settings
from syndb_api.user.model import AccessToken, User

logger = getLogger(__name__)


context = CryptContext(schemes=["argon2"], deprecated="auto")
password_helper = PasswordHelper(context)


class BikipyUserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    reset_password_token_secret = settings.passlib_secret
    verification_token_secret = settings.passlib_secret

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger.info(f'User, UUID="{user.id}", was registered.')

    async def on_after_forgot_password(self, user: User, token: str, request: Optional[Request] = None):
        logger.info(f'User, UUID="{user.id}" has forgot their password. Reset token: {token}')

    async def on_after_request_verify(self, user: User, token: str, request: Optional[Request] = None):
        logger.info(f'Verification requested for user, UUID="{user.id}". Verification token: {token}')


async def get_user_db(session: AsyncSession = Depends(get_db_write_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_access_token_db(
    session: AsyncSession = Depends(get_db_write_async_session),
):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)


async def get_user_manager(
    user_db=Depends(get_user_db),
) -> AsyncGenerator[BikipyUserManager, None]:
    yield BikipyUserManager(user_db, password_helper)


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=3600)


database_auth_backend = AuthenticationBackend(
    name="database",
    transport=BearerTransport(tokenUrl="user/auth/database/login"),
    get_strategy=get_database_strategy,
)

bikipy_fastapi_users = FastAPIUsers[User, UUID](get_user_manager, [database_auth_backend])
