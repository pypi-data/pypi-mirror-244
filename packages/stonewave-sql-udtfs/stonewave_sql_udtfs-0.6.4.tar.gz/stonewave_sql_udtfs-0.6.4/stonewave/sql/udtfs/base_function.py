def udtf(is_lookup=False, is_parser=False, not_producing_multi_rows=False):
    """
    @param is_parser: `is_parser=True` indicates this table function parses its argument and produces key value pairs as a new row. It should NOT write more than 1 row for each input if specified. Specifying it to be True helps performance.
    @param is_lookup: `is_lookup=True` indicates this table function uses its argument as lookup key and produces key value pairs as a new row. It should NOT write more than 1 row for each input if specified. Specifying it to be True helps performance.
    @param not_producing_multi_rows: `not_producing_multi_rows=True` indicates this table function produces no more than one row. It should NOT write more than 1 row for each input if specified.
    """

    def decorate_with_udtf(func_class):
        func_class.is_parser = is_parser
        func_class.is_lookup = is_lookup
        func_class.not_producing_multi_rows = is_lookup or is_parser or not_producing_multi_rows
        return func_class

    return decorate_with_udtf


class BaseFunction(object):
    def get_name(self):
        """
        :return: the name of the table function
        """
        return "base"

    def initialize(self, table_writer):
        """
        This method will be called once for every batch in the input table with function applied
        :param table_writer: the table writer for writing produced results
        :return: None
        """
        pass

    def process(self, params, table_writer, context):
        """
        This method is used to process input parameters, and it will be called once for every row
        when using apply operator;
        :param params: a list containing all parameters
        :param table_writer: Use the `table_writer` to write the produced results into the result table.
            `table_writer` has three writing mode:
                - row oriented
                - column oriented
                - batch oriented
            in a function process, single writing mode is required. related apis are:
                - write_row(kv_pairs) (all values are turned into string type)
                - write_column(column_name, column_type, [column_values])
                - batch_iterator
        :param context: context that maintaining more information, which is reserved for future
        :return: None
        """
        pass


BaseFunction.is_parser = False
BaseFunction.is_lookup = False
BaseFunction.not_producing_multi_rows = False
