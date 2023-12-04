from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from syndb_api.common.tags import Tags
from syndb_api.database.setup import get_db_read_async_session, get_db_write_async_session
from syndb_api.neurodata.metadata.constants import GET_ALL_PREFIX
from syndb_api.neurodata.metadata.tag.schema import (
    AllTagsJustRead,
    AnimalModelCreateRead,
    BrainRegionCreateRead,
    MicroscopyCreateRead,
    MutationModelCreateRead,
    PublicationCreateRead,
)
from syndb_api.neurodata.metadata.tag.workflow import fetch_all_tags
from syndb_api.neurodata.model import Animal, BrainRegion, Microscopy, Mutation, Publication

tag_router = APIRouter(tags=[Tags.tag])


@tag_router.get(GET_ALL_PREFIX, response_model=AllTagsJustRead, status_code=status.HTTP_200_OK)
async def fetch_all_tags_endpoint(
    cutoff_creation_datetime: Optional[datetime] = None,
    session: AsyncSession = Depends(get_db_read_async_session),
):
    return await fetch_all_tags(session, cutoff_creation_datetime)


@tag_router.post("/animal/create", status_code=status.HTTP_201_CREATED)
async def create_animal(
    create_animal_model: AnimalModelCreateRead,
    session: AsyncSession = Depends(get_db_write_async_session),
):
    new_tag = Animal(**create_animal_model.model_dump(exclude_unset=True))
    session.add(new_tag)
    await session.commit()


@tag_router.post("/brain_region/create", status_code=status.HTTP_201_CREATED)
async def create_brain_region(
    create_brain_region_model: BrainRegionCreateRead,
    session: AsyncSession = Depends(get_db_write_async_session),
):
    new_tag = BrainRegion(**create_brain_region_model.model_dump(exclude_unset=True))
    session.add(new_tag)
    await session.commit()


@tag_router.post("/mutation/create", status_code=status.HTTP_201_CREATED)
async def create_mutation(
    create_mutation_model: MutationModelCreateRead,
    session: AsyncSession = Depends(get_db_write_async_session),
):
    new_tag = Mutation(**create_mutation_model.model_dump(exclude_unset=True))
    session.add(new_tag)
    await session.commit()


@tag_router.post("/microscopy/create", status_code=status.HTTP_201_CREATED)
async def create_microscopy(
    create_microscopy_model: MicroscopyCreateRead,
    session: AsyncSession = Depends(get_db_write_async_session),
):
    new_tag = Microscopy(**create_microscopy_model.model_dump(exclude_unset=True))
    session.add(new_tag)
    await session.commit()


@tag_router.post("/publication/create", status_code=status.HTTP_201_CREATED)
async def create_publication(
    create_publication_model: PublicationCreateRead,
    session: AsyncSession = Depends(get_db_write_async_session),
):
    new_tag = Publication(**create_publication_model.model_dump(exclude_unset=True))
    session.add(new_tag)
    await session.commit()
