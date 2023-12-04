from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


dataset_dataset_collection_association_table = Table(
    "dataset_dataset_collection_association_table",
    Base.metadata,
    Column("dataset_id", ForeignKey("dataset.id")),
    Column(
        "dataset_collection_name",
        ForeignKey("dataset_collection.name"),
        primary_key=True,
    ),
)


dataset_collection_group_association_table = Table(
    "dataset_collection_group_association_table",
    Base.metadata,
    Column(
        "dataset_collection_name",
        ForeignKey("dataset_collection.name"),
        primary_key=True,
    ),
    Column("group_name", ForeignKey("owner_group.name"), primary_key=True),
)


from syndb_api.neurodata.model import *  # noqa:  E402, F401, F403
from syndb_api.user.model import *  # noqa:  E402, F401, F403
