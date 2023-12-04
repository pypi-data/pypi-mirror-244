from typing import Optional
from uuid import UUID

from fastapi_users import schemas

from syndb_api.common.schema import OrmSchemaModel, SchemaModel


class UserProfile(SchemaModel):
    id: UUID
    scientist_tag: str
    profile_picture_link: Optional[str] = None
    is_superuser: bool


class UserJustRead(OrmSchemaModel, schemas.BaseUser[UUID]):
    pass


class UserCreate(OrmSchemaModel, schemas.BaseUserCreate):
    pass


class UserUpdate(OrmSchemaModel, schemas.BaseUserUpdate):
    pass
