import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from syndb_api.database.mock import mock_dataset_a, mock_dataset_b, mock_dataset_c
from syndb_api.database.setup import DataInDB
from syndb_api.neurodata.metadata.dataset.schema import CreateDataset, DatasetSearchModel, FilterDataset
from syndb_api.neurodata.metadata.dataset.workflow import (
    dataset_tag_search,
    fetch_all_datasets_id2label,
    fetch_modifiable_datasets,
    id_to_label,
)


async def _search_and_find_mock_dataset(
    sqlalchemy_session: AsyncSession,
    dataset_search: DatasetSearchModel,
    dataset: CreateDataset,
) -> None:
    assert await dataset_tag_search(
        sqlalchemy_session,
        dataset_search,
    ) == id_to_label([dataset])


async def test_fetch_datasets(sqlalchemy_session: AsyncSession, setup_test_postgres: DataInDB) -> None:
    assert await fetch_all_datasets_id2label(sqlalchemy_session) == setup_test_postgres.datasets_id_to_label


async def test_fetch_modifiable_datasets(sqlalchemy_session: AsyncSession, setup_test_postgres: DataInDB) -> None:
    assert (
        await fetch_modifiable_datasets(sqlalchemy_session, setup_test_postgres.user.id)
        == setup_test_postgres.datasets_id_to_label
    )


@pytest.mark.asyncio
async def test_dataset_tag_search_find_multiple(sqlalchemy_session, setup_test_postgres) -> None:
    assert (
        await dataset_tag_search(
            sqlalchemy_session,
            DatasetSearchModel(
                include=FilterDataset(
                    syndb_tables=frozenset(
                        {
                            *setup_test_postgres.dataset_a.syndb_tables,
                            *setup_test_postgres.dataset_b.syndb_tables,
                            *setup_test_postgres.dataset_c.syndb_tables,
                        }
                    ),
                )
            ),
        )
        == setup_test_postgres.datasets_id_to_label
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("dataset", [mock_dataset_a, mock_dataset_b, mock_dataset_c])
class TestDatasetSearch:
    async def test_dataset_tag_search_by_publication_doi(self, sqlalchemy_session, dataset: CreateDataset):
        await _search_and_find_mock_dataset(
            sqlalchemy_session,
            DatasetSearchModel(include=FilterDataset(publication_dois=dataset.publication_dois)),
            dataset,
        )

    async def test_dataset_tag_search_by_syndb_table(self, sqlalchemy_session: AsyncSession, dataset: CreateDataset):
        await _search_and_find_mock_dataset(
            sqlalchemy_session,
            DatasetSearchModel(include=FilterDataset(syndb_tables=dataset.syndb_tables)),
            dataset,
        )

    async def test_dataset_tag_search_by_brain_structure(
        self, sqlalchemy_session: AsyncSession, dataset: CreateDataset
    ):
        await _search_and_find_mock_dataset(
            sqlalchemy_session,
            DatasetSearchModel(include=FilterDataset(brain_regions=[dataset.brain_region])),
            dataset,
        )

    async def test_dataset_tag_search_by_microscopy(self, sqlalchemy_session: AsyncSession, dataset: CreateDataset):
        await _search_and_find_mock_dataset(
            sqlalchemy_session,
            DatasetSearchModel(include=FilterDataset(microscopy_names=[dataset.microscopy.name])),
            dataset,
        )

    async def test_dataset_tag_search_by_animal_species(self, sqlalchemy_session: AsyncSession, dataset: CreateDataset):
        await _search_and_find_mock_dataset(
            sqlalchemy_session,
            DatasetSearchModel(include=FilterDataset(animal_species=[dataset.animal.species])),
            dataset,
        )

    async def test_dataset_tag_search_by_animal_cultural_name(
        self, sqlalchemy_session: AsyncSession, dataset: CreateDataset
    ):
        await _search_and_find_mock_dataset(
            sqlalchemy_session,
            DatasetSearchModel(include=FilterDataset(animal_cultural_names=[dataset.animal.cultural_name])),
            dataset,
        )

    async def test_dataset_tag_search_by_mutation(self, sqlalchemy_session: AsyncSession, dataset: CreateDataset):
        await _search_and_find_mock_dataset(
            sqlalchemy_session,
            DatasetSearchModel(include=FilterDataset(mutations=dataset.mutations)),
            dataset,
        )

    async def test_composite_dataset_tag_search(self, sqlalchemy_session: AsyncSession, dataset: CreateDataset):
        await _search_and_find_mock_dataset(
            sqlalchemy_session,
            DatasetSearchModel(
                include=FilterDataset(
                    publication_dois=dataset.publication_dois,
                    syndb_tables=dataset.syndb_tables,
                    animal_cultural_names=[dataset.animal.cultural_name],
                    animal_species=[dataset.animal.species],
                    mutations=dataset.mutations,
                    microscopy_names=[dataset.microscopy.name],
                    brain_regions=[dataset.brain_region],
                )
            ),
            dataset,
        )
