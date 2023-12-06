import pyarrow as pa
from stonewave.sql.udtfs.logger import logger
from stonewave.sql.udtfs.union_type_resolver import (
    primitive_union_data_type,
    build_primitive_union_column,
)


class RecordBatchBuilder(object):
    def __init__(self):
        self.columns = {}
        self.schema = {}
        self._row_count = 0
        self._new_rows_count = 0
        self._current_process_row_count = 0

    def column_names(self):
        return self.schema.keys()

    def add_column(self, column_name, data_type=primitive_union_data_type):
        """
        Append a column to the builder. If the column with the same name exists in the builder, it will NOT be added again.
        :param column_name: the name of the column, default value is predefined union data type
                            given a specific data type is recommended so that the function would be more effective.
                            in case the data type is not determined or the column is mixed type,
                            leave the parameter None to make it load union data type.
        :param data_type: pyarrow's field data type, for example, pyarrow::utf8()
        :return: None
        """
        if column_name not in self.columns:
            self.columns[column_name] = []
            self.schema[column_name] = data_type
            self.fill_equal_length_for_all_builders(self._current_process_row_count)
        else:
            if self.schema[column_name] != data_type:
                raise Exception(
                    "Please keep type as before for column '{}': {}".format(column_name, self.schema[column_name])
                )

    def append(self, column, value):
        """
        Append a new value for a given column.
        :param column: the name of the column
        :param value: the new value to be append to the column
        :return:
        """
        current_col_length = len(self.columns.get(column)) + 1
        if self._row_count < current_col_length:
            self._row_count = current_col_length
        return self.columns.get(column).append(value)

    def extend(self, column, values):
        """
        Append multiple new values for a new given column.
        :param column: the name of the column
        :param values: a list of new values to be appended to the columns
        :return:
        """
        current_col_length = len(self.columns.get(column)) + len(values)
        if self._row_count < current_col_length:
            self._row_count = current_col_length
        return self.columns.get(column).extend(values)

    def num_fields(self):
        """
        :return: the number of fields (columns) currently in this builder
        """
        return len(self.schema)

    def flush(self):
        """
        Flush the contents in the record build to build a record batch.
        return the record batch built from the contents in the builder,
        and return None if the built record batch is empty.
        """
        if self.columns:
            self.fill_equal_length_for_all_builders(self._current_process_row_count)
            logger.debug(
                "flushing contents from record batch builder",
                columns=len(self.columns),
                row_count=self._row_count,
            )

            arrow_arrays = [
                build_primitive_union_column(array)
                if self.schema[col].equals(primitive_union_data_type)
                else pa.array(array, self.schema[col])
                for col, array in self.columns.items()
            ]

            batch = pa.RecordBatch.from_arrays(arrow_arrays, list(self.columns.keys()))
            # clear all arrays
            for col in self.columns.keys():
                self.columns[col] = []
            self._row_count = 0
            return batch
        # having null rows only, use empty batch to indicates this
        elif self._row_count > 0:
            self._row_count = 0
            batch = pa.RecordBatch.from_arrays([])
            return batch
        else:
            return None

    def row_count(self):
        """
        Return the number of rows in the builder
        :return:
        """
        return self._row_count

    def append_null_row(self):
        """
        append a null row to the builder.
        The row count will be automatically maintained.
        :return:
        """
        for array in self.columns.values():
            array.append(None)
        self._row_count += 1

    def append_row(self, kv_pairs):
        """
        Append a row with as key value pairs, represented by a Python dictionary.
        The key represents the column name and the value represents the column value, which is pyarrow.utf8() type
        :param kv_pairs: the row's field names and values
        :return:
        """
        for key, value in kv_pairs.items():
            # TODO: we don't support creating multi value field yet in python
            self.add_column(key, pa.utf8())
            array = self._get_column_array(key)
            array.append(str(value))
        self._row_count += 1
        self.fill_equal_length_for_all_builders(self._row_count)

    def fill_equal_length_for_all_builders(self, count):
        for array in self.columns.values():
            null_count = count - len(array)
            for _ in range(0, null_count):
                array.append(None)

    def _get_column_array(self, column):
        return self.columns.get(column)

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
        self._current_process_row_count = self.row_count()

    def _after_process(self):
        self._new_rows_count = self.row_count() - self._current_process_row_count
        self.fill_equal_length_for_all_builders(self.row_count())

    def _after_equal_length_process(self, i):
        if self.row_count() <= i:
            self.append_null_row()
