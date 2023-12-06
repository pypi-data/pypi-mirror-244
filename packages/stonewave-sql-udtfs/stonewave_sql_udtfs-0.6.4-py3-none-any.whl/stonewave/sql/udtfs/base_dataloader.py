import os
import pathlib
from stonewave.sql.udtfs.logger import logger
from stonewave.sql.udtfs.constants import STONEWAVE_HOME


class BaseDataloader(object):
    def __init__(self):

        self.external_data_dir = os.path.join(STONEWAVE_HOME, "var", "external_data")

    def set_path(self, path):
        logger.debug(
            "executing set_path in base dataloader",
            path=path,
            external_data_dir=self.external_data_dir,
        )
        if os.path.isabs(path):
            abs_path = path
        else:
            abs_path = os.path.join(self.external_data_dir, path)

        data_path = os.path.realpath(abs_path)
        external_data_length = len(self.external_data_dir)

        if len(data_path) < external_data_length or data_path[:external_data_length] != self.external_data_dir:
            raise Exception("failed to load path {}: no data or directory exists in external data path.".format(path))

        data_path = pathlib.Path(data_path)

        if not data_path.exists():
            raise Exception("failed to load path {}: no such data or directory.".format(data_path))

        self.path = data_path

    def get_path(self):
        return self.path
