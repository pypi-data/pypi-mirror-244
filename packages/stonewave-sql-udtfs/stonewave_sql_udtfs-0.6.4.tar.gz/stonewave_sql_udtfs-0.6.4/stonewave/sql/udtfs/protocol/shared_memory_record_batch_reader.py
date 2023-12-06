from multiprocessing import shared_memory
import pyarrow as pa
from multiprocessing.shared_memory import SharedMemory
from multiprocessing.resource_tracker import unregister
from stonewave.sql.udtfs.logger import logger
from threading import local


# Adding the shm objects into a class variable of thread local essentially makes the shm objects available during the entire lifetime of the process/thread,
# otherwise, the program still works but Python will complain `BufferError: memoryview has 1 exported buffer`
# when releasing the shared memory object.
# The shm objects will be released after the process/thread is terminated, while the buffer in shared memory is managed by the shared memory creator (C++ process)
class ThreadLocalSharedMemoryObjects(object):
    local_data = local()

    @classmethod
    def stash(cls, shm):
        if not getattr(ThreadLocalSharedMemoryObjects.local_data, "shms", None):
            ThreadLocalSharedMemoryObjects.local_data.shms = []
        ThreadLocalSharedMemoryObjects.local_data.shms.append(shm)


class SharedMemoryRecordBatchReader(object):
    shared_memory_objects = local()

    def __init__(self, shm_name, shm_size):
        self.shm = SharedMemory(shm_name, create=False, size=shm_size)
        ThreadLocalSharedMemoryObjects.stash(self.shm)
        unregister("/" + self.shm.name, "shared_memory")

    def read(self):
        # TODO: figure out if pa.py_buffer(shm.buf) makes any difference
        with pa.ipc.open_stream(self.shm.buf) as reader:
            batches = list(reader)
            assert len(batches) == 1
            batch = batches[0]
        if batch is not None:
            logger.debug(
                "read record batch via shared memory",
                num_rows=batch.num_rows,
                num_columns=batch.num_columns,
            )
        return batch
