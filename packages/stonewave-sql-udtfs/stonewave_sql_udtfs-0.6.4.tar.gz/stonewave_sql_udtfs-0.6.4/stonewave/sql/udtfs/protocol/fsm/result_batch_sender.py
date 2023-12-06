from stonewave.sql.udtfs.protocol import ipc
from stonewave.sql.udtfs.logger import logger


class SharedMemoryRecordBatchSender(object):
    def send(self, batch):
        logger.debug(
            "send record batch via shared memory",
            num_rows=batch.num_rows,
            num_columns=batch.num_columns,
        )
        shm_info = ipc.share_record_batch(batch)
        # respond({"shm_name": shm_info[0], "shm_size": shm_info[1]})
        return {"shm_name": shm_info[0], "shm_size": shm_info[1]}
