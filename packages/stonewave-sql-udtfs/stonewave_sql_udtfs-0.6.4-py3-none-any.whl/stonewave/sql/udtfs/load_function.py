import importlib
import inspect
from stonewave.sql.udtfs.base_function import BaseFunction
from stonewave.sql.udtfs.logger import logger
from stonewave.sql.udtfs.singleton import singleton
from stonewave.sql.udtfs.constants import (
    USER_DEFINED_TABLE_FUNCTIONS_PATH,
    USER_DEFINED_TABLE_FUNCTIONS_VERSION_INFO_FILE,
)
import os


@singleton
class function_loader:
    def __init__(self):
        self.reset()

    def reset(self):
        importlib.invalidate_caches()
        self.version_map = {}

    def _find_base_function_from_lib(self, lib):
        for mod in dir(lib):
            method = eval("lib." + mod)
            if inspect.isclass(method):
                if issubclass(method, BaseFunction):
                    if not issubclass(BaseFunction, method):
                        return method
        return None

    def _read_version_file(self, name):
        file_path = os.path.join(
            USER_DEFINED_TABLE_FUNCTIONS_PATH, name, USER_DEFINED_TABLE_FUNCTIONS_VERSION_INFO_FILE
        )
        with open(file_path, "r") as f:
            version_info = f.read()
        return version_info

    ### get registered version and cached, if version not the same, reload module.
    def check_and_cache_lib_version(self, name):
        try:
            result = False
            module_version = self._read_version_file(name)
            cached_version = self.version_map.get(name)
            if cached_version is not None:
                logger.debug(
                    "compare versions of user defined table function",
                    function_name=name,
                    cached_version=cached_version,
                    module_version=module_version,
                )
                result = cached_version != module_version
            self.version_map[name] = module_version
            return result
        except Exception as e:
            logger.error("error occured in check and store hash version", detail=str(e))
            return False

    def load_function_by_name(self, name):
        try:
            # built-in table functions
            lib = importlib.import_module("stonewave.sql.udtfs.functions.{}".format(name))
            logger.debug("load built-in table function", function_name=name)
            return self._find_base_function_from_lib(lib)
        except:
            try:
                # user defined table functions
                # functions path has been append to sys.path when starting the executor

                lib = importlib.import_module(name)
                if self.check_and_cache_lib_version(name):
                    lib = importlib.reload(lib)
                logger.debug("load user defined table function", function_name=name)
                return self._find_base_function_from_lib(lib)
            except Exception as e:
                self.reset()
                raise Exception("failed to load function '{}': {}. reset cache".format(name, str(e)))
