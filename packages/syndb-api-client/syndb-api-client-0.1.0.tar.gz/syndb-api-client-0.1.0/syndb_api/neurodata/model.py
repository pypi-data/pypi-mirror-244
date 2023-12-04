from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from neurometa.constant import BrainStructure as BrainStructureEnum
from neurometa.constant import GeneExpression, NeuroanatomicalDirection
from sqlalchemy import TIMESTAMP, Boolean, Column, Enum, ForeignKey, Integer, String, Table, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from syndb_constants.table import SyndbTable
from uuid6 import uuid7

from syndb_api.database.base_model import (
    Base,
    dataset_collection_group_association_table,
    dataset_dataset_collection_association_table,
)

if TYPE_CHECKING:
    from syndb_api.user.model import OwnerGroup, User


dataset_publication_association_table = Table(
    "dataset_publication_association_table",
    Base.metadata,
    Column(
        "publication_doi",
        ForeignKey("publication.doi", ondelete="restrict"),
        primary_key=True,
    ),
    Column("dataset_id", ForeignKey("dataset.id")),
)
user_publication_association_table = Table(
    "user_publication_association_table",
    Base.metadata,
    Column("doi", ForeignKey("publication.doi"), primary_key=True),
    Column("user_id", ForeignKey("user.id")),
)


class BaseMetadata:
    created_on: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )


class Publication(BaseMetadata, Base):
    """
    link -> https://doi.org/{doi}
    """

    __tablename__ = "publication"

    doi: Mapped[str] = mapped_column(primary_key=True)

    datasets: Mapped[list["Dataset"]] = relationship(
        back_populates="publications", secondary=dataset_publication_association_table
    )
    authors: Mapped[list["User"]] = relationship(
        back_populates="publications", secondary=user_publication_association_table
    )


animal_mutation_association_table = Table(
    "animal_mutation_association_table",
    Base.metadata,
    Column(
        "animal_species",
        ForeignKey("animal.species", ondelete="restrict"),
        primary_key=True,
    ),
    Column("mutation_id", ForeignKey("mutation.id")),
)


class Animal(BaseMetadata, Base):
    __tablename__ = "animal"

    species: Mapped[str] = mapped_column(String(length=100), primary_key=True)
    cultural_name: Mapped[Optional[str]] = mapped_column(index=True)

    mutations: Mapped[list["Mutation"]] = relationship(
        back_populates="animals", secondary=animal_mutation_association_table
    )

    datasets: Mapped[list["Dataset"]] = relationship(back_populates="animal")


dataset_mutation_association_table = Table(
    "dataset_mutation_association_table",
    Base.metadata,
    Column("dataset_id", ForeignKey("dataset.id")),
    Column("mutation_id", ForeignKey("mutation.id", ondelete="restrict")),
)


class Mutation(BaseMetadata, Base):
    __tablename__ = "mutation"

    id: Mapped[UUID] = mapped_column(default=uuid7, primary_key=True)

    gene: Mapped[str] = mapped_column(String(length=100), nullable=False, index=True)
    expression: Mapped[GeneExpression] = mapped_column(Enum(GeneExpression), nullable=False, index=True)

    animals: Mapped[list["Animal"]] = relationship(
        back_populates="mutations", secondary=animal_mutation_association_table
    )
    datasets: Mapped[list["Dataset"]] = relationship(
        back_populates="mutations", secondary=dataset_mutation_association_table
    )

    __table_args__ = (UniqueConstraint("gene", "expression", name="single_instance_of_gene_type"),)


class Microscopy(BaseMetadata, Base):
    __tablename__ = "microscopy"

    name: Mapped[str] = mapped_column(String(length=200), primary_key=True)

    datasets: Mapped[list["Dataset"]] = relationship(back_populates="microscopy")


class BrainRegion(BaseMetadata, Base):
    __tablename__ = "brain_region"

    id: Mapped[UUID] = mapped_column(default=uuid7, primary_key=True)

    brain_structure: Mapped[BrainStructureEnum]
    direction: Mapped[NeuroanatomicalDirection]

    datasets: Mapped[list["Dataset"]] = relationship(back_populates="brain_region")

    __table_args__ = (UniqueConstraint("brain_structure", "direction", name="Brain regions are unique"),)

    @hybrid_property
    def name(self):
        return f"{self.direction}-{self.brain_structure}"


class BaseDataCollection(BaseMetadata):
    notes: Mapped[Optional[str]] = mapped_column(String(length=280), default=None, nullable=True)

    updated_on: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )

    owner_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), index=True)


class DatasetCollection(BaseDataCollection, Base):
    __tablename__ = "dataset_collection"

    name: Mapped[str] = mapped_column(primary_key=True)

    owner: Mapped["User"] = relationship(back_populates="owned_dataset_collections")
    authorized_groups: Mapped[list["OwnerGroup"]] = relationship(
        back_populates="authorized_dataset_collections",
        secondary=dataset_collection_group_association_table,
    )

    datasets: Mapped[list["Dataset"]] = relationship(
        back_populates="dataset_collections",
        secondary=dataset_dataset_collection_association_table,
    )


dataset_group_association_table = Table(
    "dataset_group_association_table",
    Base.metadata,
    Column("group_name", ForeignKey("owner_group.name"), primary_key=True),
    Column("dataset_id", ForeignKey("dataset.id")),
)


class Dataset(BaseDataCollection, Base):
    __tablename__ = "dataset"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    label: Mapped[str] = mapped_column(String(length=120), default=None, nullable=True)

    owner: Mapped["User"] = relationship(back_populates="owned_datasets")
    authorized_groups: Mapped[list["OwnerGroup"]] = relationship(
        back_populates="authorized_datasets", secondary=dataset_group_association_table
    )

    dataset_collections: Mapped[list[DatasetCollection]] = relationship(
        back_populates="datasets",
        secondary=dataset_dataset_collection_association_table,
        primaryjoin=dataset_dataset_collection_association_table.c.dataset_id == id,
        secondaryjoin=dataset_dataset_collection_association_table.c.dataset_collection_name == DatasetCollection.name,
    )

    upload_complete: Mapped[bool] = mapped_column(Boolean(), default=False)
    number_of_units: Mapped[int] = mapped_column(Integer(), default=0)

    # Tags
    syndb_tables: Mapped[list[SyndbTable]] = mapped_column(
        ARRAY(Enum(SyndbTable), dimensions=1), nullable=False, index=True
    )

    microscopy_name: Mapped[str] = mapped_column(ForeignKey("microscopy.name"), index=True)
    microscopy: Mapped[Microscopy] = relationship(back_populates="datasets")

    animal_species: Mapped[str] = mapped_column(ForeignKey("animal.species"), nullable=False, index=True)
    animal: Mapped[Animal] = relationship(back_populates="datasets")

    brain_region_id: Mapped[UUID] = mapped_column(
        ForeignKey("brain_region.id", ondelete="restrict"), nullable=False, index=True
    )
    brain_region: Mapped[BrainRegion] = relationship("BrainRegion", back_populates="datasets")

    mutations: Mapped[list[Mutation]] = relationship(
        back_populates="datasets", secondary=dataset_mutation_association_table
    )
    publications: Mapped[list[Publication]] = relationship(
        back_populates="datasets", secondary=dataset_publication_association_table
    )

    def __init__(self, *args, **kwargs):
        syndb_tables = kwargs.get("syndb_tables", [])
        if not syndb_tables or len(syndb_tables) == 0:
            raise ValueError(f"At least one SyndbTable must be associated with {self.__class__.__name__}.")

        super().__init__(*args, **kwargs)
