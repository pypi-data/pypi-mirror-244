import asyncio

from syndb_api.database.pre_defined import add_pre_animal_objects

asyncio.run(add_pre_animal_objects(cluster=True))
print("Pre-defined data loaded to cluster")
