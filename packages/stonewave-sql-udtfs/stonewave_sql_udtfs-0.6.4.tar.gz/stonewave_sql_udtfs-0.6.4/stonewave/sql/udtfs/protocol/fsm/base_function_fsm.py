from stonewave.sql.udtfs.logger import logger


class BaseFunctionFsm(object):
    def __init__(self, func, batch_sender, respond):
        logger.debug("init func evaluation")
        self.func = func
        self._batch_sender = batch_sender
        self._respond = respond

    def _clean_up(self):
        self.func = None
        self._batch_sender = None
        self._respond = None
