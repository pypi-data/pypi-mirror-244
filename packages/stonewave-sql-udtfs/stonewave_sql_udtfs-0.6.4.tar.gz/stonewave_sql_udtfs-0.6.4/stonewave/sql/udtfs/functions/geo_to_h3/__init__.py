from stonewave.sql.udtfs.base_function import BaseFunction, udtf
from stonewave.sql.udtfs.logger import logger
from stonewave.sql.udtfs.utility import get_arrow_data_type_from_value
import h3


@udtf(is_parser=False)
class GeoToH3(BaseFunction):
    def get_name(self):
        """
        :return: the name of the table function
        """
        return "geo_to_h3"

    def initialize(self, table_writer):
        """
        This method will be called once for every batch in the input table with function applied
        :param table_writer: the row writer for writing produced results
        :return: None
        """
        pass

    def __init__(self):
        pass

    def process(self, params, table_writer, context):
        kv_pairs = {}
        lat = float(params[0])
        lng = float(params[1])
        row_length = len(params)
        if row_length == 3:
            res = int(params[2])
            kv_pairs["res_{}".format(res)] = h3.geo_to_h3(lat, lng, res)
        else:
            for res in range(16):
                kv_pairs["res_{}".format(res)] = h3.geo_to_h3(lat, lng, res)
        table_writer.write_row(kv_pairs)
