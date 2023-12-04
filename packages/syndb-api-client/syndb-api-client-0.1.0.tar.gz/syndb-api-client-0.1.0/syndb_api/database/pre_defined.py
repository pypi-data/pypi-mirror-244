import json
from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING

from syndb_constants.table import SyndbTable

from syndb_api.database.context import get_cluster_db_write_async_session_context, get_db_write_async_session_context

if TYPE_CHECKING:
    from syndb_api.neurodata.model import Animal

STATIC_PATH = Path(__file__).parent / "static"


logger = getLogger(__name__)


async def _load_source_to_db(source: list, cluster: bool = False) -> None:
    async with (
        get_cluster_db_write_async_session_context() if cluster else get_db_write_async_session_context() as session
    ):
        session.add_all(source)
        await session.commit()

    logger.info("Loaded animal tags to database")


def pre_syndb_table_objects() -> list[SyndbTable]:
    return [SyndbTable(syndb_table_name) for syndb_table_name in SyndbTable.__members__]


def pre_animal_objects() -> list["Animal"]:
    from syndb_api.neurodata.model import Animal

    with open(STATIC_PATH / "animal.json", "r") as in_json:
        animal_data = json.load(in_json)

    return [Animal(species=k, cultural_name=v or None) for k, v in animal_data.items()]


async def add_pre_animal_objects(cluster: bool = False) -> None:
    await _load_source_to_db(pre_animal_objects(), cluster=cluster)
