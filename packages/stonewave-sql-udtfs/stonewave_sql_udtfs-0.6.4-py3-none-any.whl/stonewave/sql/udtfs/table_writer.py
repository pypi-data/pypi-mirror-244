from sqlite3 import Row
from types import CellType
from stonewave.sql.udtfs.record_batch_builder import RecordBatchBuilder
from enum import Enum


class WRITING_MODE(Enum):
    ROW_ORIENTED = 1
    COLUMN_ORIENTED = 2
    TABLE_ORIENTED = 3


class TableWriter(object):
    """
    Use the row writer to write results produced from a table function. There are three major ways to write results:
    1) `write_row(kv_pairs)`: write the produced rows row by row with string type
    2) `write_column(column_name, column_type, values)`: write column values with specific type
    3) `table_batch_iterator`: set a list of record batches to table writer.
    The `table_batch_iterator` MUST be a generator that calling its next method will return a pyarrow's RecordBatch
    """

    def __init__(self, flushing_batch_size=8 * 1024):
        self._flushing_batch_size = flushing_batch_size
        self._record_batch_builder = RecordBatchBuilder()
        self._table_batch_iterator = None
        self._last_flushed_batch_size = 0
        self._new_rows_count = 0
        self._writing_mode = None  # ROW_ORIENTED/COLUMN_ORIENTED/BATCH_ORIENTED

    @property
    def table_batch_iterator(self):
        return self._table_batch_iterator

    def check_write_mode(self, expected_mode):
        if self._writing_mode and self._writing_mode != expected_mode:
            raise Exception("Please keep in consitent using {} API".format(self._writing_mode))
        self._writing_mode = expected_mode

    @table_batch_iterator.setter
    def table_batch_iterator(self, value):
        self.check_write_mode(WRITING_MODE.TABLE_ORIENTED)
        self._table_batch_iterator = value

    def is_not_empty(self):
        return self.table_batch_iterator or self._record_batch_builder.row_count() > 0

    def flush(self, forced=False):
        self._before_flush()
        flushed_batch = None
        if self.table_batch_iterator:
            batch = self._record_batch_builder.flush()
            if batch is not None:
                flushed_batch = batch
            else:
                try:
                    flushed_batch = next(self.table_batch_iterator)
                except StopIteration:
                    self.table_batch_iterator = None
                    return None
        elif self._is_over_flushing_size() or forced and self._record_batch_builder.row_count() > 0:
            flushed_batch = self._record_batch_builder.flush()

        self._last_flushed_batch_size = flushed_batch.num_rows if flushed_batch else 0
        self._after_flush()
        return flushed_batch

    # no type
    def write_row(self, kv_pairs):
        self.check_write_mode(WRITING_MODE.ROW_ORIENTED)
        self._record_batch_builder.append_row(kv_pairs)

    # with specified type
    def write_column(self, column_name, type, values):
        self.check_write_mode(WRITING_MODE.COLUMN_ORIENTED)
        self._record_batch_builder.add_column(column_name, type)
        self._record_batch_builder.extend(column_name, values)

    ##################################################
    # APIs below are internal and is subject to change
    ##################################################
    @property
    def new_rows_count(self):
        """
        :return: the number of new rows after processing a new row or flushing results
        """
        return self._new_rows_count

    def _before_process(self):
        self._record_batch_builder._before_process()

    def _after_process(self):
        self._record_batch_builder._after_process()
        self._new_rows_count = self._record_batch_builder.new_rows_count

    def _after_equal_length_process(self, i):
        self._record_batch_builder._after_equal_length_process(i)

    def _before_flush(self):
        self._record_batch_builder._before_process()

    def _after_flush(self):
        self._record_batch_builder._after_process()
        self._new_rows_count = self._record_batch_builder.new_rows_count + self._last_flushed_batch_size

    def _is_over_flushing_size(self):
        return self._record_batch_builder.row_count() >= self._flushing_batch_size
