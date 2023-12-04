from pydantic import BaseModel


class SchemaModel(BaseModel, frozen=True):
    pass


class OrmSchemaModel(SchemaModel, from_attributes=True):
    pass
