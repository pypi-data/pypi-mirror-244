from stonewave.sql.udtfs.table_writer import TableWriter
from stonewave.sql.udtfs.protocol.fsm.apply import _lateral_join, _get_row
from stonewave.sql.udtfs.logger import logger


def _equal_length_apply(func, left_table, column_name_qualifier, func_params):
    # this can only be used with outer apply
    # only table function writing results row by row with a batch builder can correctly function here
    right_table_writer = TableWriter()
    func.initialize(right_table_writer)

    right_table = None
    for i in range(0, left_table.num_rows):
        right_table_writer._before_process()
        row = _get_row(left_table, i, func_params)
        try:
            func.process(row, right_table_writer, i)
        except Exception as e:
            logger.debug(
                "failed to process function for equal length apply operator",
                func_name=func.get_name(),
                error=str(e),
            )
        right_table_writer._after_equal_length_process(i)
    right_table = right_table_writer.flush(forced=True)
    joined_table = _lateral_join(left_table, right_table, column_name_qualifier)
    return joined_table
