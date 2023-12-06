import pyarrow as pa
from multiprocessing import shared_memory
from multiprocessing.resource_tracker import unregister
from stonewave.sql.udtfs.protocol.shared_memory_record_batch_reader import (
    ThreadLocalSharedMemoryObjects,
)


def _get_batch_data_size(record_batch):
    mock_sink = pa.MockOutputStream()
    stream_writer = pa.RecordBatchStreamWriter(mock_sink, record_batch.schema)
    stream_writer.write_batch(record_batch)
    stream_writer.close()
    data_size = mock_sink.size()
    return data_size


# FIXME: test arrow.ipc.writer to see if we can avoid copying
def _write_batch_to_buf(record_batch, buf):
    stream = pa.FixedSizeBufferWriter(buf)
    stream_writer = pa.RecordBatchStreamWriter(stream, record_batch.schema)
    stream_writer.write_batch(record_batch)
    stream_writer.close()


def share_record_batch(record_batch):
    data_size = _get_batch_data_size(record_batch)
    shm = shared_memory.SharedMemory(create=True, size=data_size)
    _write_batch_to_buf(record_batch, pa.py_buffer(shm.buf))
    ThreadLocalSharedMemoryObjects.stash(shm)

    shm.close()
    # FIXME: we don't need to unregister shared memory and requires this Python process to outlive C++ process if Python fixes it
    # https://bugs.python.org/issue38119
    unregister("/" + shm.name, "shared_memory")
    return shm.name, data_size
