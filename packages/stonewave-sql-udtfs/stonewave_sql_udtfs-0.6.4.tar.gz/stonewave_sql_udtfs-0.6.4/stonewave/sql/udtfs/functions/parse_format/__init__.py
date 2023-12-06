import pyarrow as pa
import parse
import json
from stonewave.sql.udtfs.base_function import BaseFunction, udtf


@udtf(is_parser=True)
class ParseFormatFunction(BaseFunction):
    def __init__(self):
        self.compiled_format_cache = {}

    def get_name(self):
        return "parse_format"

    def process(self, params, table_writer, context):
        text = params[0]
        pattern_format = params[1]
        compiled_format = None
        if pattern_format in self.compiled_format_cache:
            compiled_format = self.compiled_format_cache[pattern_format]
        else:
            compiled_format = parse.compile(pattern_format)
            self.compiled_format_cache[pattern_format] = compiled_format
        extracted_values = compiled_format.parse(text)

        if extracted_values:
            for col_name in extracted_values.named:
                val = extracted_values[col_name]
                if isinstance(val, dict):
                    val = json.dumps(val)
                table_writer.write_column(col_name, pa.utf8(), [val])

            i = 0
            for v in extracted_values:
                col_name = "a" + str(i)
                i += 1
                table_writer.write_column(col_name, pa.utf8(), [v])
