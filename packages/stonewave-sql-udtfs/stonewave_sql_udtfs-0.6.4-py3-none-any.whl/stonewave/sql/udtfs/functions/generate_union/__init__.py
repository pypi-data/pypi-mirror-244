from stonewave.sql.udtfs.logger import logger
from stonewave.sql.udtfs.base_function import BaseFunction
from datetime import datetime, timezone
from stonewave.sql.udtfs.union_type_resolver import primitive_union_data_type


class GenerateUnionFunction(BaseFunction):
    data_types = [
        ("null", lambda i: None),
        ("int", lambda i: i),
        ("float", lambda i: float(i)),
        ("bool", lambda i: bool(i)),
        ("string", lambda i: str(i)),
        ("timestamp", lambda i: datetime.fromtimestamp(i / 1e6, timezone.utc)),
        ("list<string>", lambda i: [str(i)]),
    ]

    def __init__(self):
        pass

    def get_name(self):
        return "generate_union"

    def process(self, params, table_writer, context):
        rng = range(0, params[0])
        types = [i.strip() for i in params[1].split(",")]
        array = []
        for idx, data_type in enumerate(GenerateUnionFunction.data_types):
            parsed_indices = []
            for idx_ts, type_str in enumerate(types):
                if type_str == data_type[0]:
                    array.extend([data_type[1](i) for i in rng])
                    parsed_indices.append(idx_ts)
            for i in reversed(parsed_indices):
                types.pop(i)

        col_name = "generate_union"
        table_writer.write_column(col_name, primitive_union_data_type, array)
        logger.debug(
            "rows generated via generate_union",
            row_count=len(array),
        )
