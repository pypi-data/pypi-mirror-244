from functools import cached_property
from logging import getLogger

from pydantic import PostgresDsn, computed_field
from pydantic.types import FilePath

from syndb_api.settings.base import SyndbApiBaseSettings

logger = getLogger(__name__)


class SyndbApiClusterSettings(SyndbApiBaseSettings):
    require_authentication: bool = True

    app_host: str = "0.0.0.0"
    app_host_port = 8000

    postgres_write_host: str
    postgres_read_host: str

    postgres_db_name: str = "users"

    jwk_secret_path: FilePath

    @computed_field  # type: ignore[misc]
    @cached_property
    def db_write_uri(self) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.postgres_username,
            password=self.postgres_password,
            host=self.postgres_write_host,
            port=self.postgres_port,
            path=self.postgres_path,
        )

    @computed_field  # type: ignore[misc]
    @cached_property
    def db_read_uri(self) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.postgres_username,
            password=self.postgres_password,
            host=self.postgres_read_host,
            port=self.postgres_port,
            path=self.postgres_path,
        )
