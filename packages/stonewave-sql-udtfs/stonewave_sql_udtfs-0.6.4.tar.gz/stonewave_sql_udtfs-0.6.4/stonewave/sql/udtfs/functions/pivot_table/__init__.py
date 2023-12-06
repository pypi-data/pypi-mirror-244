from stonewave.sql.udtfs.base_function import BaseFunction
import pyarrow as pa
import pandas as pd


class PivotTableFunction(BaseFunction):
    def __init__(self):
        self.tables = []
        self.x_field = None
        self.y_name_field = None
        self.y_data_fields = None
        self.fill_value = None

    def get_name(self):
        return "pivot_table"

    def process(self, params, table_writer, context):
        if self.x_field == None and len(params) < 4:
            raise Exception(
                "Table function 'pivot_table' parameter invalid: "
                "parameter should be (data_set_name, index_field, "
                "column_name, column_values)"
            )
        batch = params[0]
        if batch is not None:
            self.x_field = params[1]
            self.y_name_field = params[2]
            self.y_data_fields = list(map(str.strip, params[3].split(",")))
            self.fill_value = float(params[4]) if len(params) >= 5 else None
            table = pa.Table.from_batches([batch])
            self.tables.append(table)
        else:
            self.pivot(table_writer)

    def pivot(self, table_writer):
        if self.tables:
            table = pa.concat_tables(self.tables, promote=True)
            df = table.to_pandas()
            for f in self.y_data_fields:
                if f not in df:
                    raise Exception(
                        "Table function 'pivot_table' parameter invalid: " "column '{}' not exist".format(f)
                    )
                if not pd.api.types.is_numeric_dtype(df[f]):
                    df[f] = pd.to_numeric(df[f], "coerce")
            pvt = pd.pivot_table(
                df,
                values=self.y_data_fields,
                index=self.x_field,
                columns=self.y_name_field,
                fill_value=self.fill_value,
            )

            if len(self.y_data_fields) == 1:
                pvt.columns = [x[1] for x in pvt.columns]
            else:
                pvt.columns = ["{}${}".format(x[0], x[1]) for x in pvt.columns]
            pvt = pvt.reset_index()
            table = pa.Table.from_pandas(pvt, preserve_index=False)
            # make timestamp schema as us unit
            fields = []
            for s in table.schema:
                if pa.types.is_timestamp(s.type):
                    fields.append(pa.field(s.name, pa.timestamp("us")))
                else:
                    fields.append(s)
            table = pa.table(table.columns, pa.schema(fields))
            batches = table.to_batches()
            table_writer.table_batch_iterator = iter(batches)
        else:
            return
