import os

PROCESS_ERROR_MSG_TEMPLATE = "Table function process failed: function '{}', {}"
VALIDATE_ERROR_MSG_TEMPLATE = "parameters type should be [{}]"

STONEWAVE_HOME = os.environ.get("STONEWAVE_HOME", "/tmp")
USER_DEFINED_TABLE_FUNCTIONS_MODULE = "py_udtfs"
USER_DEFINED_TABLE_FUNCTIONS_PATH = os.path.join(STONEWAVE_HOME, "var", USER_DEFINED_TABLE_FUNCTIONS_MODULE)
USER_DEFINED_TABLE_FUNCTION_INFO_FILE = "info.toml"
USER_DEFINED_TABLE_FUNCTIONS_VERSION_INFO_FILE = "register_version_info_signature"
SIGNATURE_LIST = "signature_list"

# for ci tests
if not os.path.exists(USER_DEFINED_TABLE_FUNCTIONS_PATH):
    os.makedirs(USER_DEFINED_TABLE_FUNCTIONS_PATH)


class ParameterType:
    LITERAL = "literal"
    COLUMN = "column"
    TYPE = "type"
    VALUE = "value"


class ParameterDataType:
    STRING = "STRING"
    INT = "INT"
    FLOAT = "FLOAT"
    BOOL = "BOOL"
    TABLE = "TABLE"

    def with_default_value(datatype, default_val):
        return "{} = {}".format(datatype, default_val)
