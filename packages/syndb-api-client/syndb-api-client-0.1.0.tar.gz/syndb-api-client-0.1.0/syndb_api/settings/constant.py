from syndb_api import IN_CLUSTER
from syndb_api.settings.local import SyndbApiAlembicSettings

if IN_CLUSTER:
    from syndb_api.settings.cluster import SyndbApiClusterSettings

    settings = SyndbApiClusterSettings()

else:
    from syndb_api.settings.local import SyndbApiLocalSettings

    settings = SyndbApiLocalSettings()


cluster_settings = SyndbApiAlembicSettings()


def set_settings(**new_settings):
    global settings
    for k, v in new_settings.items():
        settings.__setattr__(k, v)
