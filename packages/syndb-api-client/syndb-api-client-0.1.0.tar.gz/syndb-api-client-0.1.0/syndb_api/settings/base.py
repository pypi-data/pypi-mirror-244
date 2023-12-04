from abc import ABC, abstractmethod
from functools import cached_property
from logging import getLogger
from typing import ClassVar

from httpx_oauth.oauth2 import OAuth2
from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine


logger = getLogger(__name__)


class SyndbApiBaseSettings(BaseSettings, ABC):
    debug: bool = False

    app_name: str = "SynapseDB User API"

    app_host: str = "127.0.0.1"
    app_host_port: int = 8180
    app_root_path: str | None = None

    scylla_url: str

    postgres_username: str
    postgres_password: str
    postgres_port: int = 5432
    postgres_path: str

    s3_access_key: str
    s3_secret_key: str

    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite
    # https://www.starlette.io/responses/#set-cookie
    cookie_same_site: str = "strict"
    cookie_secure: bool = True

    require_authentication: bool

    jwt_seconds_to_live: int = 21600  # 30 minutes
    upload_timeout: int = 21600  # 6 hours

    passlib_secret: str

    syndb_tortoise_model_module: ClassVar[str] = "syndb_api.orm.models"

    @property
    @abstractmethod
    def db_write_uri(self) -> PostgresDsn:
        ...

    @property
    @abstractmethod
    def db_read_uri(self) -> PostgresDsn:
        ...

    def db_write_engine(self, **kwargs):
        return create_async_engine(str(self.db_write_uri), **kwargs)

    def db_read_engine(self, **kwargs):
        return create_async_engine(str(self.db_read_uri), **kwargs)

    @computed_field  # type: ignore[misc]
    @cached_property
    def host_path(self) -> str:
        return f"{self.app_host}:{self.app_host_port}"
