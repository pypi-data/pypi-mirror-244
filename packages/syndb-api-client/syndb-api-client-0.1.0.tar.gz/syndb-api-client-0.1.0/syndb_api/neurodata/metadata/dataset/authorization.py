from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from syndb_api.neurodata.model import Dataset


async def dataset_exists(session: AsyncSession, dataset_id: UUID, error_if_not: bool = True) -> bool:
    result = await session.scalar(select(exists().where(Dataset.id == dataset_id)))
    if error_if_not and not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset, with ID={dataset_id}, could not be found",
        )
    return result
