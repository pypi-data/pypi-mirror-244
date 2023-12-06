from stonewave.sql.udtfs.base_function import BaseFunction, udtf
import importlib


# ssh_public_key ==> SshPublicKey
def _to_camel_case(snake_str):
    components = snake_str.split("_")
    return "".join([c.capitalize() for c in components])


# TODO: how can we combine with the arrow dataset with this function?


@udtf(is_parser=True)
class ParseBinaryFunction(BaseFunction):
    def __init__(self):
        pass

    def get_name(self):
        return "parse_binary"

    def process(self, params, table_writer, context):
        file_path = params[0]
        format_name = params[1]
        data_paths = [c.strip() for c in params[2].split(",")] if len(params) > 2 else []
        kaitai_parser = "stonewave.sql.udtfs.functions.parse_binary.formats.{}".format(format_name)
        module = importlib.import_module(kaitai_parser)
        parser_class_name = _to_camel_case(format_name)
        parser_class = getattr(module, parser_class_name)
        # TODO: there is some security concern, we probably need to limit the path it can access
        parsed_binary = parser_class.from_file(file_path)
        kv_pairs = {}
        for path in data_paths:
            # TODO: can we marshall it into a JSON string?
            value = str(getattr(parsed_binary, path))
            kv_pairs[path] = value
        table_writer.write_row(kv_pairs)
