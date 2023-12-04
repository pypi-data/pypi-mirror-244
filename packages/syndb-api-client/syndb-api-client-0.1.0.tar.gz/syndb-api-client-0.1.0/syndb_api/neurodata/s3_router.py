from uuid import UUID

from botocore.client import BaseClient
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from syndb_api.common.constant import S3_BUCKET_NAME_MESH
from syndb_api.common.s3 import (
    PreSignedS3Schema,
    generate_pre_signed_directory_upload,
    generate_pre_signed_s3_upload,
    get_s3_client,
)
from syndb_api.common.tags import Tags
from syndb_api.database.setup import get_db_write_async_session
from syndb_api.neurodata.metadata.dataset.workflow import confirm_user_modifiable_dataset
from syndb_api.user.manager import bikipy_fastapi_users
from syndb_api.user.model import User

s3_router = APIRouter(tags=[Tags.s3])


@s3_router.post(
    "/upload/mesh",
    name="upload_mesh",
    response_model=PreSignedS3Schema,
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.s3],
)
async def upload_dataset_mesh(
    dataset_id: UUID,
    s3: BaseClient = Depends(get_s3_client),
    session: AsyncSession = Depends(get_db_write_async_session),
    user: User = Depends(bikipy_fastapi_users.current_user(active=True)),
) -> PreSignedS3Schema:
    await confirm_user_modifiable_dataset(session, dataset_id, user.id)
    return await generate_pre_signed_directory_upload(s3, S3_BUCKET_NAME_MESH, str(dataset_id), "model/gltf-binary")


@s3_router.post(
    "/upload/swb",
    name="upload_swb",
    response_model=PreSignedS3Schema,
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.s3],
)
async def upload_dataset_swb(
    dataset_id: UUID,
    s3: BaseClient = Depends(get_s3_client),
    session: AsyncSession = Depends(get_db_write_async_session),
    user: User = Depends(bikipy_fastapi_users.current_user(active=True)),
) -> PreSignedS3Schema:
    await confirm_user_modifiable_dataset(session, dataset_id, user.id)
    return await generate_pre_signed_s3_upload(s3, S3_BUCKET_NAME_MESH, f"{dataset_id}/", "text/plain")
