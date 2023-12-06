import pyarrow as pa
from datetime import datetime

_primitive_data_types = [
    (type(None), pa.null()),
    (int, pa.int64()),
    (float, pa.float64()),
    (bool, pa.bool_()),
    (str, pa.utf8()),
    (datetime, pa.timestamp("us")),
    (list, pa.list_(pa.utf8())),
]
primitive_union_data_type = pa.union(
    [pa.field(str(idx), dt[1]) for idx, dt in enumerate(_primitive_data_types)], "dense"
)


def build_primitive_union_column(column_values):
    type_ids = []
    offsets = []
    child_arrays = [] * 7
    for idx, type_tuple in enumerate(_primitive_data_types):
        child_array = []
        offset_starts = 0
        parsed_indices = []
        for val_idx, value in enumerate(column_values):
            if type(value) == type_tuple[0]:
                type_ids.append(idx)
                offsets.append(offset_starts)
                child_array.append(value)
                offset_starts += 1
                parsed_indices.append(val_idx)
        for i in reversed(parsed_indices):
            column_values.pop(i)
        child_arrays.append(pa.array(child_array, type=type_tuple[1]))
    return pa.UnionArray.from_dense(
        pa.array(type_ids, type=pa.int8()),
        pa.array(offsets, type=pa.int32()),
        child_arrays,
    )
