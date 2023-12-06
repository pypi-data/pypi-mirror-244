from stonewave.sql.udtfs.base_function import BaseFunction
import pyarrow as pa


class UnpivotTableFunction(BaseFunction):
    def __init__(self):
        self.tables = []
        self.x_field = None
        self.y_name_field = None
        self.y_data_field = None

    def get_name(self):
        return "unpivot_table"

    def process(self, params, table_writer, context):
        if self.x_field == None and len(params) < 4:
            raise Exception(
                "Table function 'unpivot_table' parameter invalid: "
                "parameter should be (data_set_name, index_field, "
                "column_name, column_value_name)"
            )
        batch = params[0]
        if batch is not None:
            self.x_field = params[1]
            self.y_name_field = params[2]
            self.y_data_field = params[3]
            table = pa.Table.from_batches([batch])
            # FIXME: the current implementation caches all batches, which is not necessary
            self.tables.append(table)
        else:
            self.unpivot(table_writer)

    def unpivot(self, table_writer):
        if self.tables:
            table = pa.concat_tables(self.tables, promote=True)
            df = table.to_pandas()
            unpvt = df.melt(
                id_vars=self.x_field,
                var_name=self.y_name_field,
                value_name=self.y_data_field,
            )
            unpvt_table = pa.Table.from_pandas(unpvt, preserve_index=False)
            batches = unpvt_table.to_batches()
            table_writer.table_batch_iterator = iter(batches)
        else:
            return
