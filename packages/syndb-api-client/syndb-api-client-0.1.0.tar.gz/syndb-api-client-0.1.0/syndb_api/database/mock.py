from neurometa.constant import BrainStructure as BrainStructureEnum
from neurometa.constant import GeneExpression, NeuroanatomicalDirection
from sqlalchemy.ext.asyncio import AsyncSession
from syndb_constants.table import SyndbTable

from syndb_api import IN_CLUSTER
from syndb_api.neurodata.metadata.dataset.schema import CreateDataset
from syndb_api.neurodata.metadata.dataset.workflow import ensure_tags_and_create_dataset
from syndb_api.neurodata.metadata.tag.schema import (
    AnimalModelCreateRead,
    BrainRegionCreateRead,
    MicroscopyCreateRead,
    MutationModelCreateRead,
)
from syndb_api.neurodata.model import Dataset
from syndb_api.user.model import User

mock_dataset_a = CreateDataset(
    notes="This is for a test",
    label="MyTestDataset",
    publication_dois=frozenset({"s43587-023-00368-3"}),
    syndb_tables=frozenset({SyndbTable.VESICLE}),
    brain_region=BrainRegionCreateRead(brain_structure=BrainStructureEnum.CA2, direction=NeuroanatomicalDirection.NULL),
    mutations=[MutationModelCreateRead(gene="ABC", expression=GeneExpression.OVEREXPRESSION)],
    microscopy=MicroscopyCreateRead(name="STED"),
    animal=AnimalModelCreateRead(species="Rattus norvegicus", cultural_name="Rat"),
)
mock_dataset_b = CreateDataset(
    notes="This is for a test",
    label="MyTestDataset",
    publication_dois=frozenset({"s43587-023-00368-2"}),
    syndb_tables=frozenset({SyndbTable.MITOCHONDRIA}),
    brain_region=BrainRegionCreateRead(brain_structure=BrainStructureEnum.CA1, direction=NeuroanatomicalDirection.NULL),
    mutations=[MutationModelCreateRead(gene="ACD", expression=GeneExpression.KNOCK_IN)],
    microscopy=MicroscopyCreateRead(name="LEM"),
    animal=AnimalModelCreateRead(species="Brachydanio rerio", cultural_name="Zebrafish"),
)
mock_dataset_c = CreateDataset(
    notes="This is for a test",
    label="MyTestDataset",
    publication_dois=frozenset({"s43587-023-00368-1"}),
    syndb_tables=frozenset({SyndbTable.AXON}),
    brain_region=BrainRegionCreateRead(brain_structure=BrainStructureEnum.CA3, direction=NeuroanatomicalDirection.NULL),
    mutations=[MutationModelCreateRead(gene="AD", expression=GeneExpression.OVEREXPRESSION)],
    microscopy=MicroscopyCreateRead(name="Confocal"),
    animal=AnimalModelCreateRead(species="Mus musculus", cultural_name="Mouse"),
)


async def register_mock_datasets(session: AsyncSession, owner: User) -> tuple[Dataset, Dataset, Dataset]:
    _no_mock_in_cluster()

    dataset_a = await ensure_tags_and_create_dataset(session, owner, mock_dataset_a)
    await session.commit()

    dataset_b = await ensure_tags_and_create_dataset(session, owner, mock_dataset_b)
    await session.commit()

    dataset_c = await ensure_tags_and_create_dataset(session, owner, mock_dataset_c)
    await session.commit()

    return dataset_a, dataset_b, dataset_c


def _no_mock_in_cluster():
    if IN_CLUSTER:
        raise AttributeError("Mock data must not be committed in production")
