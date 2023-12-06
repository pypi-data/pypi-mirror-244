import importlib.metadata

package_metadada = importlib.metadata.metadata("stonewave-sql-udtfs")
# info from pyproject.toml's `version`
VERSION = package_metadada.get("Version")


def sql_udtfs_version():
    return VERSION
