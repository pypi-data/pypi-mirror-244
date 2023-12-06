import pyarrow as pa

from stonewave.sql.udtfs.table_writer import TableWriter
from stonewave.sql.udtfs.logger import logger
from stonewave.sql.udtfs.protocol.fsm.shared_record_batch_reader import (
    read_record_batch,
)
from stonewave.sql.udtfs.protocol.fsm.apply import _lateral_join, _get_row
from stonewave.sql.udtfs.protocol.fsm.apply.equal_length_apply import (
    _equal_length_apply,
)
from stonewave.sql.udtfs.protocol.fsm.apply.apply_left_table_builder import (
    ApplyLeftTableBuilder,
)


class ApplyOperator(object):
    def __init__(self, func, params, flushing_batch_size=8 * 1024):
        self._func = func
        self._params = params
        self._flushing_batch_size = flushing_batch_size

    def execute(self):
        """
        params will contain the info about left table for apply operation, it is a shared memory name and size
        params will contains other parameters when calling the APPLY
        For example, `APPLY parse_regex(_message, regex_pattern)`, the params will be: [{shm_name, shm_size}, is_outer_apply, column_name_qualifier, {expr}, {expr}]
        """
        assert len(self._params) > 1
        shm_info = self._params[0]
        left_table = read_record_batch(shm_info)
        is_outer_apply = self._params[1]
        column_name_qualifier = self._params[2]
        func_params = self._params[3:]

        if is_outer_apply and self._func.__class__.not_producing_multi_rows:
            yield _equal_length_apply(
                self._func,
                left_table,
                column_name_qualifier,
                func_params,
            )
        else:
            yield from _generic_apply_func(
                self._func,
                left_table,
                is_outer_apply,
                column_name_qualifier,
                func_params,
                self._flushing_batch_size,
            )


def _generic_apply_func(
    func,
    left_table,
    is_outer_apply,
    column_name_qualifier,
    func_params,
    flushing_batch_size,
):
    left_table_builder = ApplyLeftTableBuilder(left_table)
    rwriter = TableWriter(flushing_batch_size)

    for i in range(0, left_table.num_rows):
        yield from _process_row(
            i,
            func,
            is_outer_apply,
            func_params,
            left_table,
            left_table_builder,
            rwriter,
            column_name_qualifier,
        )

    # if there is remaining non flushed contents in the right table
    if rwriter.is_not_empty():
        logger.debug(
            "force flushing the remaining right table",
            batch_iterator=rwriter.table_batch_iterator,
        )
        right_table = rwriter.flush(True)
        if right_table:
            logger.debug("remaining right table flushed", right_table_size=right_table.num_rows)
        yield _lateral_join(
            left_table_builder.flush(),
            right_table,
            column_name_qualifier,
        )


def _process_row(
    i,
    func,
    is_outer_apply,
    func_params,
    left_table,
    lbuilder,
    rwriter,
    column_name_qualifier,
):
    initial_total_repeats = lbuilder.get_total_repeats()

    rwriter._before_process()
    try:
        if i == 0:
            func.initialize(rwriter)
        row = _get_row(left_table, i, func_params)
        func.process(row, rwriter, i)

        rwriter._after_process()
        lbuilder.repeat(i, rwriter.new_rows_count)

        while True:
            right_table = rwriter.flush(forced=False)
            if _has_only_null_rows(right_table):
                yield lbuilder.flush()
                continue
            lbuilder.repeat(i, rwriter.new_rows_count)

            if right_table:
                joined_table = _lateral_join(
                    lbuilder.flush(),
                    right_table,
                    column_name_qualifier,
                )
                yield joined_table
            else:
                break
    except Exception as e:
        logger.error(
            "failed to process row",
            function=func.get_name(),
            args=func_params,
            error=str(e),
        )

    # no right table row is produced after processing this left table row
    if is_outer_apply and lbuilder.get_total_repeats() == initial_total_repeats:
        lbuilder.repeat(i, 1)
        rwriter._record_batch_builder.append_null_row()
    logger.debug("row processed", row_idx=i, left_table_length=lbuilder.get_total_repeats())


# when a number of null rows are appended to the builder, the flushed right table will be an empty batch
# this could happen when apply is outer apply, and the previous row(s) produces empty rows
def _has_only_null_rows(right_table):
    return right_table is not None and right_table.num_rows == 0
