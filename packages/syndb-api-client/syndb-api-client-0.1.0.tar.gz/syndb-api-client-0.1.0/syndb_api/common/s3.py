from typing import Any, AsyncGenerator, Optional

import aioboto3
from aioboto3.session import ResourceCreatorContext
from botocore import config
from botocore.client import BaseClient
from pydantic import Field

from syndb_api.common.schema import SchemaModel
from syndb_api.settings.constant import settings

connection_kwargs = dict(
    service_name="s3",
    endpoint_url="https://s3-west.nrp-nautilus.io",
    aws_access_key_id=settings.s3_access_key,
    aws_secret_access_key=settings.s3_secret_key,
    config=config.Config(signature_version="s3v4"),
)


async def get_s3_client() -> AsyncGenerator[BaseClient, None]:
    session = aioboto3.Session()
    async with session.client(**connection_kwargs) as s3_client:
        yield s3_client


async def get_s3_resource() -> AsyncGenerator[ResourceCreatorContext, None]:
    session = aioboto3.Session()
    async with session.resource(**connection_kwargs) as s3_resource:
        yield s3_resource


async def generate_pre_signed_s3_upload(
    s3: BaseClient,
    bucket: str,
    content_type: str,
    key_prefix: Optional[str] = None,
    expires_in: int = 7200,
):
    conditions = [{"acl": "public-read", "Content-Type": content_type}]
    return await s3.generate_presigned_post(
        bucket,
        key_prefix or "",
        Conditions=conditions,
        ExpiresIn=expires_in,
    )


async def generate_pre_signed_directory_upload(
    s3: BaseClient,
    bucket: str,
    directory_name: str,
    content_type: Optional[str] = None,
    expires_in: int = 7200,
):
    conditions = [
        ["starts-with", "$key", f"{directory_name}/"],
        dict(acl="public-read"),
    ]
    if content_type:
        conditions.append({"Content-Type": content_type})

    return PreSignedS3Schema(
        **await s3.generate_presigned_post(
            bucket,
            f"{directory_name}/${{filename}}",
            Fields=None,
            Conditions=conditions,
            ExpiresIn=expires_in,
        )
    )


async def pre_signed_s3_download_url(s3: BaseClient, bucket: str, key: str, expires_in: int = 120) -> str:
    return await s3.generate_presigned_url("get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=expires_in)


class PreSignedS3Schema(SchemaModel):
    upload_url: str = Field(validation_alias="url")
    fields: dict[str, Any]
