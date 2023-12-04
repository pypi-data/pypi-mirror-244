from abc import ABC, abstractmethod
from typing import Iterable, Optional
from uuid import UUID

from neurometa.constant import BrainStructure as BrainStructureEnum
from neurometa.constant import GeneExpression, NeuroanatomicalDirection
from pydantic import Field, model_validator
from sqlalchemy import ColumnElement, and_, or_

from syndb_api.common.schema import SchemaModel
from syndb_api.neurodata.model import Animal, BrainRegion, Mutation


class DeepMatchSchema(SchemaModel, ABC):
    @abstractmethod
    def match_expression(self) -> ColumnElement[bool]:
        ...

    @abstractmethod
    def unmatch_expression(self) -> ColumnElement[bool]:
        ...


def inclusive_match_expression(
    iterable: Iterable[DeepMatchSchema],
) -> ColumnElement[bool]:
    return or_(s.match_expression() for s in iterable)


def inclusive_unmatch_expression(
    iterable: Iterable[DeepMatchSchema],
) -> ColumnElement[bool]:
    return or_(s.unmatch_expression() for s in iterable)


class AnimalModelJustRead(DeepMatchSchema):
    species: Optional[str] = None
    cultural_name: Optional[str] = None

    @model_validator(mode="before")
    def species_and_or_cultural(cls, values):
        if "species" not in values and "cultural_name" not in values:
            raise ValueError("Either species or cultural name of animal must be defined")
        return values

    def match_expression(self) -> ColumnElement[bool]:
        if self.species or self.cultural_name:
            return Animal.species == self.species
        if self.cultural_name:
            return Animal.cultural_name == self.cultural_name

        raise RuntimeError("Should not arrive at this line WRT validation")

    def unmatch_expression(self) -> ColumnElement[bool]:
        if self.species or self.cultural_name:
            return Animal.species != self.species
        if self.cultural_name:
            return Animal.cultural_name != self.cultural_name

        raise RuntimeError("Should not arrive at this line WRT validation")


class AnimalModelCreateRead(SchemaModel):
    species: str
    cultural_name: Optional[str]


class _MutationIO(DeepMatchSchema):
    def match_expression(self) -> ColumnElement[bool]:
        if self.gene and self.expression:
            return and_(Mutation.gene == self.gene, Mutation.expression == self.expression)
        if self.gene:
            return Mutation.gene == self.gene
        if self.expression:
            return Mutation.expression == self.expression

    def unmatch_expression(self) -> ColumnElement[bool]:
        if self.gene and self.expresion:
            return and_(Mutation.gene != self.gene, Mutation.expression != self.expression)
        if self.gene:
            return Mutation.gene != self.gene
        if self.expression:
            return Mutation.expression != self.expression


class MutationModelJustRead(_MutationIO):
    gene: Optional[str] = None
    expression: Optional[GeneExpression] = None


class MutationModelCreateRead(_MutationIO):
    id: Optional[UUID] = None

    gene: str
    expression: GeneExpression


class _BrainRegionIO(DeepMatchSchema):
    def match_expression(self) -> ColumnElement[bool]:
        if self.brain_structure and self.direction:
            return and_(
                BrainRegion.brain_structure == self.brain_structure,
                BrainRegion.direction == self.direction,
            )
        if self.brain_structure:
            return BrainRegion.brain_structure == self.brain_structure
        if self.direction:
            return BrainRegion.direction == self.direction

    def unmatch_expression(self) -> ColumnElement[bool]:
        if self.brain_structure and self.direction:
            return and_(
                BrainRegion.brain_structure != self.brain_structure,
                BrainRegion.direction != self.direction,
            )
        if self.brain_structure:
            return BrainRegion.brain_structure != self.brain_structure
        if self.direction:
            return BrainRegion.direction != self.direction


class BrainRegionJustRead(_BrainRegionIO):
    brain_structure: Optional[BrainStructureEnum] = None
    direction: Optional[NeuroanatomicalDirection] = None


class BrainRegionCreateRead(_BrainRegionIO):
    id: Optional[UUID] = None

    brain_structure: BrainStructureEnum
    direction: NeuroanatomicalDirection


class _MicroscopyIO(SchemaModel):
    name: str


class MicroscopyJustRead(_MicroscopyIO):
    pass


class MicroscopyCreateRead(_MicroscopyIO):
    pass


class _PublicationIO(SchemaModel):
    doi: str


class PublicationJustRead(_PublicationIO):
    pass


class PublicationCreateRead(_PublicationIO):
    pass


class AllTagsJustRead(SchemaModel):
    animal: Optional[list[AnimalModelJustRead]] = Field(default_factory=list)
    brain_region: Optional[list[BrainRegionJustRead]] = Field(default_factory=list)
    mutation: Optional[list[MutationModelJustRead]] = Field(default_factory=list)
    microscopy_names: Optional[list[str]] = Field(default_factory=list)
    publication_dois: Optional[list[str]] = Field(default_factory=list)
