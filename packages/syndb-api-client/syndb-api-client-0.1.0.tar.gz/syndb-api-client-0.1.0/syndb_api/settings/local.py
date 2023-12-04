from functools import cached_property

from pydantic import PostgresDsn, computed_field

from syndb_api.settings.base import SyndbApiBaseSettings


class SyndbApiLocalSettings(SyndbApiBaseSettings):
    require_authentication: bool = False

    scylla_url: str = "127.0.0.1"

    postgres_host: str = "127.0.0.1"

    postgres_path: str = "syndb_test"
    postgres_username: str = "syndb"
    postgres_password: str = "syndb"

    s3_access_key: str = "YJJUYYT6KTE9FQUY8J95"
    s3_secret_key: str = "WpsyrHFIpJvOl7RCECPUSHdXVBADiDaDBxEcXC1p"

    cookie_same_site: str = "none"
    passlib_secret: str = "not_passlib_secret"

    @computed_field  # type: ignore[misc]
    @cached_property
    def db_write_uri(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.postgres_username,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            path=self.postgres_path,
        )

    @computed_field  # type: ignore[misc]
    @property
    def db_read_uri(self) -> str:
        return self.db_write_uri


class SyndbApiAlembicSettings(SyndbApiLocalSettings):
    postgres_username: str = "ufastapi"
    postgres_password: str = "XP2DGHCwrd8Qz2Ws2rvv1JgreiwSn1cpfqqlMl72BIibyZYAwzb7jh1sWBOl9Cid"

    # postgres_write_host: str = "67.58.49.48"
    postgres_write_host: str = "127.0.0.1"
    postgres_port: int = 15432
    postgres_path: str = "syndb"
