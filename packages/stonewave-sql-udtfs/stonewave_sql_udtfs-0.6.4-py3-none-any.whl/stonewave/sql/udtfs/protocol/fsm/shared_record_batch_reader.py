from stonewave.sql.udtfs.protocol.shared_memory_record_batch_reader import (
    SharedMemoryRecordBatchReader,
)


def read_record_batch(shm_info):
    shm_name, shm_size = shm_info["shm_name"], shm_info["shm_size"]
    batch = None
    # an empty shm_name indicates there is no batch passed into the function
    if shm_name:
        reader = SharedMemoryRecordBatchReader(shm_name, shm_size)
        batch = reader.read()
    return batch
