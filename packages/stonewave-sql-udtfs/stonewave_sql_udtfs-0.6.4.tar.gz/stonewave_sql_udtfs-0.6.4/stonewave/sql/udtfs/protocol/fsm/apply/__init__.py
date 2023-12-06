import pyarrow as pa
from stonewave.sql.udtfs.protocol.arrow import rename_duplicated_field
from stonewave.sql.udtfs.logger import logger

# left table and right table must have the exact same number of rows
def _lateral_join(left_table, right_table, column_name_qualifier):
    if right_table and right_table.num_columns > 0:
        right_table_schema = right_table.schema
        result_schema = left_table.schema
        arrays = [array for array in left_table]
        for i in range(0, right_table.num_columns):
            field = right_table_schema.field(i)
            field_name = column_name_qualifier + "." + field.name if column_name_qualifier else field.name
            field = pa.field(field_name, field.type)
            field = rename_duplicated_field(result_schema, field)
            result_schema = result_schema.append(field)
            arrays.append(right_table.column(i))
        result_table = pa.RecordBatch.from_arrays(arrays, result_schema.names)
        logger.debug(
            "lateral join left and right tables",
            num_rows=result_table.num_rows,
            num_columns=result_table.num_columns,
        )
        return result_table
    else:
        logger.debug(
            "lateral join with empty right table, return left table as it is",
            left_table=left_table.num_rows,
        )
        return left_table


def _get_cell_value_by_param(batch, row_id, param):
    param_type = param["type"]
    param_value = param["value"]
    if param_type == "literal":
        return param_value
    elif param_type == "column":
        column_name = param_value
        column_index = batch.schema.get_field_index(column_name)
        if column_index == -1:
            # column does not exist, return None
            return None
        column = batch[column_index]
        return column[row_id].as_py()
    return None


def _get_row(batch, row_id, params):
    row = [_get_cell_value_by_param(batch, row_id, param) for param in params]
    return row
