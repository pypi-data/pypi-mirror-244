from enum import Enum


class Tags(Enum):
    auth = "auth"
    superuser = "superuser"
    user = "user"

    neurodata = "neurodata"
    metadata = "metadata"
    dataset = "dataset"
    dataset_collection = "dataset_collection"
    tag = "tag"
    stargate = "stargate"

    s3 = "s3"

    crud_router = "crud_router"
