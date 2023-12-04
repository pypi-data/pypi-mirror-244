from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from syndb_api.common.tags import Tags
from syndb_api.database.setup import get_db_read_async_session, get_db_write_async_session
from syndb_api.neurodata.metadata.constants import GET_ALL_PREFIX
from syndb_api.neurodata.metadata.dataset.schema import (
    CreateDataset,
    CreateReadDatasetCollectionModel,
    DatasetSearchModel,
)
from syndb_api.neurodata.metadata.dataset.workflow import (
    dataset_tag_search,
    ensure_tags_and_create_dataset,
    fetch_all_datasets_id2label,
    fetch_modifiable_datasets,
    register_dataset_upload_completion,
)
from syndb_api.neurodata.metadata.schema import Id2LabelResponse, IdResponse
from syndb_api.neurodata.model import DatasetCollection
from syndb_api.user.manager import bikipy_fastapi_users
from syndb_api.user.model import User

dataset_router = APIRouter(tags=[Tags.dataset])


@dataset_router.post("/new_dataset", response_model=IdResponse)
async def register_new_dataset(
    create_dataset: CreateDataset,
    session: AsyncSession = Depends(get_db_write_async_session),
    user: User = Depends(bikipy_fastapi_users.current_user(active=True)),
):
    await ensure_tags_and_create_dataset(session, user, create_dataset)
    await session.commit()

    return IdResponse(id=create_dataset.id)


@dataset_router.get(
    GET_ALL_PREFIX,
    name="fetch_all_datasets_id2label",
    response_model=Id2LabelResponse,
)
async def fetch_all_datasets_endpoint(
    session: AsyncSession = Depends(get_db_read_async_session),
) -> Id2LabelResponse:
    return Id2LabelResponse(uuid_to_label=await fetch_all_datasets_id2label(session))


@dataset_router.get(
    "/{scientist_tag}",
    description="Datasets belonging to scientist tag",
    response_model=Id2LabelResponse,
)
async def scientist_tag_datasets(
    scientist_tag: str, session: AsyncSession = Depends(get_db_read_async_session)
) -> Id2LabelResponse:
    # TODO
    pass


@dataset_router.get(
    "/modifiable",
    name="fetch_modifiable_datasets",
    response_model=Id2LabelResponse,
)
async def fetch_modifiable_datasets_endpoint(
    session: AsyncSession = Depends(get_db_read_async_session),
    user: User = Depends(bikipy_fastapi_users.current_user(active=True)),
) -> Id2LabelResponse:
    return Id2LabelResponse(uuid_to_label=await fetch_modifiable_datasets(session, user.id))


@dataset_router.post("/dataset_tag_search", response_model=Id2LabelResponse)
async def dataset_tag_search_endpoint(
    dataset_search_model: DatasetSearchModel,
    session: AsyncSession = Depends(get_db_read_async_session),
) -> Id2LabelResponse:
    return Id2LabelResponse(uuid_to_label=await dataset_tag_search(session, dataset_search_model))


@dataset_router.put(
    "/upload_complete",
    name="register_dataset_upload_completion",
    status_code=status.HTTP_200_OK,
)
async def register_dataset_upload_completion_endpoint(
    dataset_id: UUID,
    upload_size: int,
    session: AsyncSession = Depends(get_db_write_async_session),
) -> None:
    await register_dataset_upload_completion(dataset_id, upload_size, session)


@dataset_router.post(
    "/new_dataset_collection",
    status_code=status.HTTP_201_CREATED,
)
async def new_dataset_collection(
    create_dc: CreateReadDatasetCollectionModel,
    session: AsyncSession = Depends(get_db_write_async_session),
    user: User = Depends(bikipy_fastapi_users.current_user(active=True)),
):
    dataset_collection = DatasetCollection(**create_dc.model_dump(exclude_unset=True), owner_id=user.id)

    session.add(dataset_collection)
    await session.commit()
    await session.refresh(dataset_collection)
