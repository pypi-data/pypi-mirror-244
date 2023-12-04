import subprocess

from syndb_api.main import app

# NOTE: 3.1 is not supported yet: https://github.com/orgs/OpenAPITools/projects/4
app.openapi_version = "3.0.3"

try:
    from ruamel.yaml import YAML
except ModuleNotFoundError as e:
    raise ValueError("Install ruamel.yaml first") from e


repo_root = (
    subprocess.Popen(["git", "rev-parse", "--show-toplevel"], stdout=subprocess.PIPE).communicate()[0].decode().strip()
)
with open(f"{repo_root}/openapi.yaml", "w") as out_yaml:
    YAML().dump(app.openapi(), out_yaml)
