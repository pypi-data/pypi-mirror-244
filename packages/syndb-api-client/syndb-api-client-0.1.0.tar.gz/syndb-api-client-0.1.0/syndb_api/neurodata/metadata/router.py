from fastapi import APIRouter

from syndb_api.common.tags import Tags
from syndb_api.neurodata.metadata.dataset.router import dataset_router
from syndb_api.neurodata.metadata.tag.router import tag_router

metadata_router = APIRouter(tags=[Tags.metadata])

metadata_router.include_router(dataset_router, prefix="/dataset")
metadata_router.include_router(tag_router, prefix="/tag")
