import os
from importlib import metadata

PACKAGE_NAME: str = "syndb_api"

IN_CLUSTER: bool = bool(os.environ.get("IN_CLUSTER", False))

# Using split to get to the name of the main module
package_version = metadata.version(__name__.split(".")[0])
