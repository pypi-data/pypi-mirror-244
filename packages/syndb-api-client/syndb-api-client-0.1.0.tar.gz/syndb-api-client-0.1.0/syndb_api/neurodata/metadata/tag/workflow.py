from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from syndb_api.neurodata.metadata.tag.schema import (
    AllTagsJustRead,
    AnimalModelJustRead,
    BrainRegionJustRead,
    MutationModelJustRead,
)
from syndb_api.neurodata.model import Animal, BrainRegion, Microscopy, Mutation, Publication


async def fetch_all_animals(
    session: AsyncSession, cutoff_creation_datetime: Optional[datetime] = None
) -> list[AnimalModelJustRead]:
    statement = select(Animal.species, Animal.cultural_name)
    if cutoff_creation_datetime:
        statement.where(Animal.created_on > cutoff_creation_datetime)
    return [AnimalModelJustRead(species=i[0], cultural_name=i[1]) for i in await session.execute(statement)]


async def fetch_all_brain_regions(
    session: AsyncSession, cutoff_creation_datetime: Optional[datetime] = None
) -> list[BrainRegionJustRead]:
    statement = select(BrainRegion.brain_structure, BrainRegion.direction)
    if cutoff_creation_datetime:
        statement.where(BrainRegion.created_on > cutoff_creation_datetime)

    return [BrainRegionJustRead(brain_structure=i[0], direction=i[1]) for i in await session.execute(statement)]


async def fetch_all_mutations(
    session: AsyncSession, cutoff_creation_datetime: Optional[datetime] = None
) -> list[MutationModelJustRead]:
    statement = select(Mutation.gene, Mutation.expression)
    if cutoff_creation_datetime:
        statement.where(Mutation.created_on > cutoff_creation_datetime)

    return [MutationModelJustRead(gene=i[0], expression=i[1]) for i in await session.execute(statement)]


async def fetch_all_microscopy_methods(
    session: AsyncSession, cutoff_creation_datetime: Optional[datetime] = None
) -> list[str]:
    statement = select(Microscopy.name)
    if cutoff_creation_datetime:
        statement.where(Microscopy.created_on > cutoff_creation_datetime)

    return [i[0] for i in await session.execute(statement)]


async def fetch_all_publications(
    session: AsyncSession, cutoff_creation_datetime: Optional[datetime] = None
) -> list[str]:
    statement = select(Publication.doi)
    if cutoff_creation_datetime:
        statement.where(Publication.created_on > cutoff_creation_datetime)

    return [i[0] for i in await session.execute(statement)]


async def fetch_all_tags(session: AsyncSession, cutoff_creation_datetime: Optional[datetime] = None) -> AllTagsJustRead:
    return AllTagsJustRead(
        animal=await fetch_all_animals(session, cutoff_creation_datetime),
        brain_region=await fetch_all_brain_regions(session, cutoff_creation_datetime),
        mutation=await fetch_all_mutations(session, cutoff_creation_datetime),
        microscopy_names=await fetch_all_microscopy_methods(session, cutoff_creation_datetime),
        publication_dois=await fetch_all_publications(session, cutoff_creation_datetime),
    )
