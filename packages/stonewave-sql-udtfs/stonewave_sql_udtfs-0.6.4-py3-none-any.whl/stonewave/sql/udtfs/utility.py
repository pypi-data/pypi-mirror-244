import pyarrow as pa
from stonewave.sql.udtfs.constants import ParameterDataType as pdt


def get_arrow_data_type_from_value(value):
    if value is None:
        return pa.utf8()
    else:
        # bool needs to be placed before int because isinstance(True, int) == True
        if isinstance(value, bool):
            return pa.bool_()
        elif isinstance(value, int):
            return pa.int64()
        elif isinstance(value, float):
            return pa.float64()
        # elif isinstance(value, decimal.Decimal):
        # return pa.decimal128(13)
        else:
            return pa.utf8()


def get_arrow_data_type(type):
    if type == pdt.STRING:
        return pa.utf8()
    elif type == pdt.FLOAT:
        return pa.float64()
    elif type == pdt.INT:
        return pa.int64()
    elif type == pdt.BOOL:
        return pa.bool_()
    else:
        return pa.utf8()
