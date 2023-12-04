from typing import Optional
from uuid import UUID

from pydantic import Field
from sqlalchemy import CompoundSelect, Select, and_, not_, select, union_all
from syndb_constants.table import SyndbTable
from uuid6 import uuid7

from syndb_api.common.schema import OrmSchemaModel, SchemaModel
from syndb_api.neurodata.metadata.schema import CommonMetadata
from syndb_api.neurodata.metadata.tag.schema import (
    AnimalModelCreateRead,
    BrainRegionCreateRead,
    BrainRegionJustRead,
    MicroscopyCreateRead,
    MicroscopyJustRead,
    MutationModelCreateRead,
    MutationModelJustRead,
    inclusive_match_expression,
    inclusive_unmatch_expression,
)
from syndb_api.neurodata.model import (
    Animal,
    BrainRegion,
    Dataset,
    Mutation,
    Publication,
    dataset_mutation_association_table,
    dataset_publication_association_table,
)

"""
Splitting tags based on their relationship with Dataset. Tags that have many to many relationships with Dataset
can be in CommonDatasetModel as they are Many in the Search Model anyway. Tags with Many to One relationships
must be split, Many in Search One in Create
"""


class CommonDatasetModel(CommonMetadata):
    dataset_collection_names: Optional[list[str]] = Field(default_factory=list)

    syndb_tables: Optional[frozenset[SyndbTable]] = Field(default_factory=frozenset)
    publication_dois: Optional[frozenset[str]] = Field(default_factory=frozenset)


class FilterDataset(CommonDatasetModel, OrmSchemaModel):
    owner_id: Optional[list[UUID]] = Field(default_factory=list)

    animal_species: Optional[list[str]] = Field(default_factory=list)
    animal_cultural_names: Optional[list[str]] = Field(default_factory=list)

    microscopy_names: Optional[list[str]] = Field(default_factory=list)

    mutations: Optional[list[MutationModelJustRead]] = Field(default_factory=list)
    brain_regions: Optional[list[BrainRegionJustRead]] = Field(default_factory=list)
    microscopies: Optional[list[MicroscopyJustRead]] = Field(default_factory=list)


class CreateDataset(CommonDatasetModel):
    id: Optional[UUID] = Field(default_factory=uuid7)
    label: str = Field(max_length=120)
    notes: Optional[str] = None

    animal: AnimalModelCreateRead
    mutations: Optional[frozenset[MutationModelCreateRead]] = Field(default_factory=frozenset)
    brain_region: BrainRegionCreateRead
    microscopy: MicroscopyCreateRead


class DatasetSearchModel(SchemaModel):
    include: FilterDataset
    exclude: Optional[FilterDataset] = None

    def exist_in_include(self, to_check: str) -> bool:
        return bool(getattr(self.include, to_check, False))

    def exist_in_exclude(self, to_check: str) -> bool:
        return self.exclude and self.exclude and getattr(self.exclude, to_check, False)

    def check_exists(self, to_check: str) -> bool:
        return self.exist_in_include(to_check) or self.exist_in_exclude(to_check)

    def select(self) -> Select | CompoundSelect:
        where_clauses = []
        if self.check_exists("syndb_tables"):
            # && operator to determine if two arrays overlap
            if self.exist_in_include("syndb_tables"):
                where_clauses.append(Dataset.syndb_tables.op("&&")(self.include.syndb_tables))
            if self.exist_in_exclude("syndb_tables"):
                where_clauses.append(not_(Dataset.syndb_tables.op("&&")(self.exclude.syndb_tables)))

        if self.check_exists("microscopy_names"):
            if self.exist_in_include("microscopy_names"):
                where_clauses.append(Dataset.microscopy_name.in_(self.include.microscopy_names))
            if self.exist_in_exclude("microscopy_names"):
                where_clauses.append(Dataset.microscopy_name.not_in(self.exclude.microscopy_names))

        if self.check_exists("animal_species") or self.check_exists("animal_cultural_names"):
            clauses = []
            if self.check_exists("animal_species"):
                if self.exist_in_include("animal_species"):
                    clauses.append(Animal.species.in_(self.include.animal_species))
                if self.exist_in_exclude("animal_species"):
                    clauses.append(Animal.species.not_in(self.exclude.animal_species))

            if self.check_exists("animal_cultural_names"):
                if self.exist_in_include("animal_cultural_names"):
                    clauses.append(Animal.cultural_name.in_(self.include.animal_cultural_names))
                if self.exist_in_exclude("animal_cultural_names"):
                    clauses.append(Animal.cultural_name.not_in(self.exclude.animal_cultural_names))

            assert clauses

            where_clauses.append(Dataset.animal_species.in_(select(Animal.species).where(and_(*clauses)).subquery()))

        if self.check_exists("brain_regions"):
            clauses = []
            if self.exist_in_include("brain_regions"):
                clauses.append(inclusive_match_expression(self.include.brain_regions))
            if self.exist_in_exclude("brain_regions"):
                clauses.append(inclusive_unmatch_expression(self.exclude.brain_regions))

            assert clauses

            where_clauses.append(Dataset.brain_region_id.in_(select(BrainRegion.id).where(and_(*clauses)).subquery()))

        # NEED JOINS ⬇️

        filtered_dataset = select(Dataset)
        if where_clauses:
            filtered_dataset = filtered_dataset.where(and_(*where_clauses))
        filtered_dataset = filtered_dataset.cte(name="filtered_dataset")

        selects = []

        if self.check_exists("publication_dois"):
            clauses = []
            if self.exist_in_include("publication_dois"):
                clauses.append(Publication.doi.in_(self.include.publication_dois))
            if self.exist_in_exclude("publication_dois"):
                clauses.append(Publication.doi.not_in(self.exclude.publication_dois))

            assert clauses

            selects.append(
                select(filtered_dataset.c.id, filtered_dataset.c.label)
                .join(
                    dataset_publication_association_table,
                    filtered_dataset.c.id == dataset_publication_association_table.c.dataset_id,
                )
                .where(
                    select(Publication.doi).where(and_(*clauses))
                    == dataset_publication_association_table.c.publication_doi
                )
            )

        if self.check_exists("mutations"):
            clauses = []
            if self.exist_in_include("mutations"):
                clauses.append(inclusive_match_expression(self.include.mutations))
            if self.exist_in_exclude("mutations"):
                clauses.append(inclusive_unmatch_expression(self.exclude.mutations))

            assert clauses

            selects.append(
                select(filtered_dataset.c.id, filtered_dataset.c.label)
                .join(
                    dataset_mutation_association_table,
                    filtered_dataset.c.id == dataset_mutation_association_table.c.dataset_id,
                )
                .where(select(Mutation.id).where(and_(*clauses)) == dataset_mutation_association_table.c.mutation_id)
            )

        if selects:
            if len(selects) == 1:
                return selects[0]

            return union_all(*selects)

        return select(Dataset.id, Dataset.label).where(and_(*where_clauses))


class CommonDatasetCollectionModel(CommonMetadata):
    name: str
    dataset_ids: Optional[list[UUID]] = None

    notes: Optional[str] = None


class JustReadDatasetCollectionModel(CommonDatasetCollectionModel, OrmSchemaModel):
    pass


class CreateReadDatasetCollectionModel(CommonDatasetCollectionModel):
    pass


class DatasetCollectionNameResponse(SchemaModel):
    name: str


class DatasetCollectionNameListResponse(SchemaModel):
    names: list[str]
