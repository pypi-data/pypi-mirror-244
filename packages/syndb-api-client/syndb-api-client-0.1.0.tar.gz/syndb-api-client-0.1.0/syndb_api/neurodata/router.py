from logging import getLogger
from typing import Annotated
from uuid import UUID

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from scyllapy import Scylla
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from syndb_cassandra.workflow.rs import insert_dataset_into_neuro_table
from syndb_constants.table import syndb_table_name_to_enum

from syndb_api.common.tags import Tags
from syndb_api.database.setup import get_db_read_async_session, get_scylla_session
from syndb_api.neurodata.metadata.dataset.workflow import confirm_user_modifiable_dataset
from syndb_api.neurodata.metadata.router import metadata_router
from syndb_api.neurodata.s3_router import s3_router
from syndb_api.settings.constant import settings
from syndb_api.user.manager import bikipy_fastapi_users
from syndb_api.user.model import User

logger = getLogger(__name__)

neurodata_router = APIRouter(
    tags=[Tags.neurodata],
    dependencies=[Depends(bikipy_fastapi_users.current_user(active=True))] if settings.require_authentication else [],
)

neurodata_router.include_router(metadata_router, prefix="/metadata")
neurodata_router.include_router(s3_router, prefix="/s3")


@neurodata_router.post(
    "/upload_dataset_files",
    status_code=status.HTTP_201_CREATED,
    description="SynDB neurodata imaging metrics data upload endpoint",
)
async def upload_dataset_files(
    neurodata_files: Annotated[list[UploadFile], File(description="Parquet files storing SynDB neurodata")],
    dataset_id: UUID,
    user: User = Depends(bikipy_fastapi_users.current_user(active=True)),
    session: AsyncSession = Depends(get_db_read_async_session),
    scylla: Scylla = Depends(get_scylla_session),
) -> None:
    await confirm_user_modifiable_dataset(session, dataset_id, user.id)

    syndb_table_to_df = {}
    for neurodata_file in neurodata_files:
        try:
            syndb_table = syndb_table_name_to_enum[neurodata_file.filename.split(".")[0].lower()]
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"Filename: {neurodata_file.filename}; invalid syndb_table",
            )

        syndb_table_to_df[syndb_table] = pd.read_parquet(neurodata_file.file)

    try:
        await insert_dataset_into_neuro_table(scylla, syndb_table_to_df, dataset_id)
    except Exception as e:
        logger.error(error_msg := str(e))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, error_msg) from e
