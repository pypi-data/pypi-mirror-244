import pyarrow as pa
from pygrok import Grok
from stonewave.sql.udtfs.base_function import BaseFunction, udtf


@udtf(is_parser=True)
class ParseGrokFunction(BaseFunction):
    def __init__(self):
        self.grok_pattern_cache = {}

    def get_name(self):
        return "parse_grok"

    def process(self, params, table_writer, context):
        text = params[0]
        grok_pattern = params[1]

        grok = None
        if grok_pattern in self.grok_pattern_cache:
            grok = self.grok_pattern_cache[grok_pattern]
        else:
            grok = Grok(grok_pattern)
            self.grok_pattern_cache[grok_pattern] = grok
        extracted_values = grok.match(text)

        if extracted_values:
            for col_name, col_value in extracted_values.items():
                # FIXME: support more non string data types
                table_writer.write_column(col_name, pa.utf8(), [col_value])
