from typing import Optional
from uuid import UUID

from pydantic import Field

from syndb_api.common.schema import SchemaModel


class CommonMetadata(SchemaModel):
    authorized_group_names: Optional[list[str]] = Field(default_factory=list)


class IdResponse(SchemaModel):
    id: UUID


class Id2LabelResponse(SchemaModel):
    uuid_to_label: dict[UUID, str]
