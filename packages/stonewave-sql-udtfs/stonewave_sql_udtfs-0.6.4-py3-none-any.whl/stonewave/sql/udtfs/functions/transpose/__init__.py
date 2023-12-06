import pyarrow as pa
from stonewave.sql.udtfs.base_function import BaseFunction
from stonewave.sql.udtfs.logger import logger


class TransposeFunction(BaseFunction):
    def __init__(self):
        self.tables = []
        self.header_field = None

    def get_name(self):
        return "transpose"

    def process(self, params, table_writer, context):
        assert len(params) > 0
        batch = params[0]
        if batch is not None:
            if not self.header_field and len(params) == 2:
                self.header_field = params[1]
            table = pa.Table.from_batches([batch])
            self.tables.append(table)
        else:
            self.transpose(table_writer)

    def transpose(self, table_writer):
        if self.tables:
            table = pa.concat_tables(self.tables, promote=True)
            df = table.to_pandas()
            header_field_index = None
            # before transpose, remove duplicate header field value
            if self.header_field:
                if self.header_field not in df.columns:
                    raise Exception("Table function 'TRANSPOSE' parameter invalid: " "no such header field")
                header_field_index = df.columns.get_loc(self.header_field)
                df = df.drop_duplicates(subset=[self.header_field])
                logger.debug(
                    "remove duplicate field values row",
                    before_num_rows=table.num_rows,
                    after_num_rows=len(df),
                )

            # transpose
            transpose_df = df.transpose()
            transpose_df = transpose_df.reset_index()
            # find header field row index
            if header_field_index is not None:
                # promote header field as header
                new_header = transpose_df.iloc[header_field_index]
                transpose_df = transpose_df.drop(transpose_df.index[header_field_index])
                try:
                    # fill field header null value with string "NULL"
                    transpose_df.columns = new_header.fillna("NULL")
                except Exception as e:
                    raise Exception("Table function 'TRANSPOSE' parameter invalid: " "unsupported header field, %s" % e)
            else:
                transpose_df.columns = ["col_%d" % i for i in range(transpose_df.columns.size)]

            try:
                table = pa.Table.from_pandas(transpose_df, preserve_index=False)
            except pa.lib.ArrowTypeError as e:
                table = None
                self.tables = None
                raise Exception("Failed to transpose: " "there are multiple datatype in single field, %s" % str(e))
            except Exception as e:
                table = None
                self.tables = None
                raise Exception("Failed to transpose: %s" % e)
            batches = table.to_batches()
            table_writer.table_batch_iterator = iter(batches)
        else:
            return
