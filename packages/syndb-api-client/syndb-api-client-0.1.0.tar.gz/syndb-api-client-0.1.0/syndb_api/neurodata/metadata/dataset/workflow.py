from collections.abc import Hashable
from typing import Any, Iterable, Type
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import and_, inspect, select, union_all, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from starlette import status

from syndb_api.database.base_model import Base
from syndb_api.neurodata.metadata.dataset.schema import (
    CreateDataset,
    CreateReadDatasetCollectionModel,
    DatasetCollectionNameListResponse,
    DatasetSearchModel,
)
from syndb_api.neurodata.metadata.workflow import resolve_groups_from_names
from syndb_api.neurodata.model import Animal, BrainRegion, Dataset, DatasetCollection, Microscopy, Mutation, Publication
from syndb_api.user.model import OwnerGroup, User, user_group_association_table


async def _get_object_by_pk_or_create(session: AsyncSession, model: Type[Base], **kwargs: dict[str, Any]) -> Base:
    model_object = await session.scalar(
        select(model).where(and_(*(getattr(model, field) == value for field, value in kwargs.items())))
    )

    if not model_object:
        model_object = model(**kwargs)
        session.add(model_object)

    return model_object


async def _get_objects_by_pk_or_create(
    session: AsyncSession, model: Type[Base], pk_values: Iterable[Hashable]
) -> list[Base]:
    """
    Retrieve the row as object by its primary key (PK); when the row doesn't exist create the row with the PK

    Assume the PK is not composite
    """
    pk_column = inspect(model).primary_key[0]
    queries = [select(model).where(pk_column == pk_value) for pk_value in pk_values]
    scalar = await session.scalars(union_all(*queries))

    pk_to_model_objects = {}
    for pk_value, model_row in zip(pk_values, scalar):
        if pk_value in pk_to_model_objects:
            continue

        if not model_row:
            model_row = model(**{pk_column: pk_value})
            session.add(model_row)

        pk_to_model_objects[pk_value] = model_row

    return list(pk_to_model_objects.values())


async def ensure_tags_and_create_dataset(session: AsyncSession, user: User, create_dataset: CreateDataset) -> Dataset:
    with session.no_autoflush:
        mutation_objects = []
        for mutation_data in create_dataset.mutations:
            mutation = (
                await session.scalars(
                    select(Mutation).where(
                        Mutation.gene == mutation_data.gene,
                        Mutation.expression == mutation_data.expression,
                    )
                )
            ).first()

            if not mutation:
                mutation = Mutation(gene=mutation_data.gene, expression=mutation_data.expression)
                session.add(mutation)

            mutation_objects.append(mutation)

        animal_object = (
            await session.execute(select(Animal).where(Animal.species == create_dataset.animal.species))
        ).scalar()
        if not animal_object:
            animal_object = Animal(
                species=create_dataset.animal.species,
                cultural_name=create_dataset.animal.cultural_name,
            )
            session.add(animal_object)

        new_dataset = Dataset(
            id=create_dataset.id,
            label=create_dataset.label,
            notes=create_dataset.notes,
            owner_id=user.id,
            owner=user,
            authorized_groups=await resolve_groups_from_names(session, create_dataset.authorized_group_names),
            dataset_collections=(
                (
                    await session.scalars(
                        select(DatasetCollection).where(
                            DatasetCollection.name.in_(create_dataset.dataset_collection_names)
                        )
                    )
                ).all()
                if create_dataset.dataset_collection_names
                else []
            ),
            publications=await _get_objects_by_pk_or_create(session, Publication, create_dataset.publication_dois),
            syndb_tables=create_dataset.syndb_tables,
            animal_species=create_dataset.animal.species,
            animal=animal_object,
            mutations=mutation_objects,
            brain_region_id=create_dataset.brain_region.id,
            brain_region=await _get_object_by_pk_or_create(
                session,
                BrainRegion,
                **create_dataset.brain_region.model_dump(exclude_unset=True),
            ),
            microscopy_name=create_dataset.microscopy.name,
            microscopy=await _get_object_by_pk_or_create(
                session,
                Microscopy,
                **create_dataset.microscopy.model_dump(exclude_unset=True),
            ),
        )

    session.add(new_dataset)

    return new_dataset


async def dataset_tag_search(session: AsyncSession, dataset_search_model: DatasetSearchModel) -> dict[UUID, str]:
    return id_to_label(await session.execute(dataset_search_model.select()))


async def fetch_all_datasets_id2label(session: AsyncSession) -> dict[UUID, str]:
    return id_to_label(await session.execute(select(Dataset.id, Dataset.label)))


async def fetch_modifiable_datasets(session: AsyncSession, user_id: UUID) -> dict[UUID, str]:
    OwnerGroupAlias = aliased(OwnerGroup)

    statement = (
        select(Dataset.id, Dataset.label)
        .join(User, User.id == Dataset.owner_id)
        .where(User.id == user_id)
        .union_all(select(Dataset.id, Dataset.label).join(OwnerGroupAlias.authorized_datasets).join(User.groups))
        .order_by(Dataset.created_on.desc())
    )

    return id_to_label(await session.execute(statement))


async def confirm_user_modifiable_dataset(session: AsyncSession, dataset_id: UUID, user_id: UUID):
    statement = (
        select(Dataset.id)
        .where(and_(Dataset.id == dataset_id, Dataset.owner_id == user_id))
        .union_all(
            select(Dataset.id)
            .where(Dataset.id == dataset_id)
            .join(OwnerGroup.authorized_datasets)
            .join(
                user_group_association_table,
                user_group_association_table.c.group_name == OwnerGroup.name,
            )
            .where(user_group_association_table.c.user_id == user_id)
        )
        .exists()
    )

    if not await session.scalar(select(statement)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User in the current session does not have access to the dataset with ID={dataset_id}",
        )


async def register_dataset_upload_completion(dataset_id: UUID, upload_size: int, session: AsyncSession):
    await session.execute(
        update(Dataset)
        .where(Dataset.id == dataset_id)
        .values(upload_complete=True, number_of_units=Dataset.number_of_units + upload_size)
    )


def id_to_label(source: Iterable) -> dict[UUID, str]:
    return {row.id: row.label for row in source}


async def user_dataset_collections(session: AsyncSession, user_id: UUID) -> DatasetCollectionNameListResponse:
    return DatasetCollectionNameListResponse(
        names=list(await session.scalars(select(DatasetCollection.name).where(DatasetCollection.owner_id == user_id)))
    )


async def register_new_dataset_collection(
    session: AsyncSession,
    user: User,
    new_dataset_collection: CreateReadDatasetCollectionModel,
):
    session.add(
        DatasetCollection(
            name=new_dataset_collection.name,
            notes=new_dataset_collection.notes,
            owner=user,
            authorized_groups=await resolve_groups_from_names(session, new_dataset_collection.authorized_group_names),
        )
    )
    await session.commit()
