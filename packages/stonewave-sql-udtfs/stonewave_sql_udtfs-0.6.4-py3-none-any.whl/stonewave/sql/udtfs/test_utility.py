from stonewave.sql.udtfs.constants import VALIDATE_ERROR_MSG_TEMPLATE
from stonewave.sql.udtfs.constants import ParameterDataType as pdt
from stonewave.sql.udtfs.constants import ParameterType as pt
from stonewave.sql.udtfs.table_writer import TableWriter
from stonewave.sql.udtfs.protocol.ipc import share_record_batch
from stonewave.sql.udtfs.protocol.fsm.apply.apply_function import ApplyOperator
import pyarrow as pa
import pyarrow.csv as csv


def _get_expected_python_type_for_parameter_type(parameter_type):
    if parameter_type == pdt.STRING:
        return str
    if parameter_type == pdt.INT:
        return int
    if parameter_type == pdt.FLOAT:
        return float
    if parameter_type == pdt.BOOL:
        return bool


def _validate_apply_parameters(given_params, expected_parameters_list):
    """
    Validate apply table function parameter type.
    :param given_params example list [{"column_name": "column"}, {"a": "literal"}]
    :expected_parameters_list all possible parameter lists
    Will not check the column datatype, because column datatype can be auto casted by stonewave.
    Will not check the size of parameter, only check the existing parameter datatype.
    Allow default parameter for table function
    """
    for expected_params in expected_parameters_list:
        if len(given_params) == len(expected_params):
            for i in range(len(given_params)):
                if given_params[i][pt.TYPE] == pt.LITERAL:
                    expected_type = expected_params[i].split(" = ")[0].upper()
                    if not isinstance(
                        given_params[i][pt.VALUE],
                        _get_expected_python_type_for_parameter_type(expected_type),
                    ):
                        raise Exception(VALIDATE_ERROR_MSG_TEMPLATE.format(",".join(expected_params)))
            return
    raise Exception(VALIDATE_ERROR_MSG_TEMPLATE.format(",".join(expected_parameters_list)))


def _validate_eval_parameters(given_params, expected_parameters_list):
    """
    Validate evaluate table function parameter type.
    :param given_params example list ['abc', 123]
    :expected_parameters_list all possible parameter lists
    """
    for expected_params in expected_parameters_list:
        if len(given_params) == len(expected_params):
            for i in range(len(given_params)):
                expected_type = expected_params[i].split(" = ")[0].upper()
                if not isinstance(
                    given_params[i],
                    _get_expected_python_type_for_parameter_type(expected_type),
                ):
                    raise Exception(VALIDATE_ERROR_MSG_TEMPLATE.format(",".join(expected_params)))
            return
    raise Exception(VALIDATE_ERROR_MSG_TEMPLATE.format(",".join(expected_parameters_list)))


def wrap_apply_function_input_parameter_with_type(parameter_type, parameter_value):
    """
    Wrap apply function input parameter with type.
    :param parameter_type support [stonewave.sql.udtfs.constants.ParameterType.COLUMN,
           stonewave.sql.udtfs.constants.ParameterType.LITERAL]
    :param parameter_value
    :return:
    """
    return {pt.TYPE: parameter_type, pt.VALUE: parameter_value}


def check_expected_parameters_list(expected_parameters_list):
    parameters_size = set()
    for expected_params in expected_parameters_list:
        params_len = len(expected_params)
        if params_len in parameters_size:
            raise Exception(
                "Do not support same parameter list size with different datatype, because of \
                Stonewave can auto cast"
            )
        parameters_size.add(params_len)
        for i in range(len(expected_params)):
            expected_type = expected_params[i].split(" = ")[0].upper()
            if expected_type not in [
                pdt.STRING,
                pdt.INT,
                pdt.FLOAT,
                pdt.BOOL,
                pdt.TABLE,
            ]:
                raise Exception("Parameter datatype should be in one of [STRING, INT, FLOAT, BOOL, TABLE]")


def eval_table_function_test(func_method, params, expected_parameters_list):
    """
    Test for evaluate table function
    :param func_method table function method
    :param params evaluate table function input parameters, only literal supported
    :param expected_parameters_list expected parameters list
    """
    _validate_eval_parameters(params, expected_parameters_list)
    func = func_method()
    row_writer = TableWriter()
    func.process(params, row_writer, 0)
    batch = None
    begininig = True
    while begininig or batch is None:
        begininig = False
        batch = row_writer.flush(True)
        yield batch


def apply_table_function_test(func_method, left_table, is_outer_apply, params, expected_parameters_list):
    _validate_apply_parameters(params, expected_parameters_list)
    func = func_method()
    shm_info = share_record_batch(left_table)
    operator_params = [
        {"shm_name": shm_info[0], "shm_size": shm_info[1]},
        is_outer_apply,
        "",
    ]
    operator_params.extend(params)

    apply_op = ApplyOperator(func, operator_params)
    result = apply_op.execute()
    return result


def get_table_from_batch_iterator(batch_iterator):
    """
    get table from batch iterator
    :param batch_iterator:
    :return:
    """
    batches = []
    try:
        batches.append(next(batch_iterator))
    except StopIteration:
        pass
    table = pa.Table.from_batches(batches)
    return table


def check_table_results_with_csv_file(table, expected_result_csv_path):
    """
    check table results with csv file
    :param table:
    :param expected_result_csv_path:
    :return:
    """
    # empty string cell will be read as null cell
    convert_options = csv.ConvertOptions(strings_can_be_null=True)
    expected_table = csv.read_csv(expected_result_csv_path, convert_options=convert_options)
    assert table.num_rows == expected_table.num_rows
    assert table.num_columns == expected_table.num_columns
    assert table.equals(expected_table)


def read_arrow_batch_from_csv(csv_pth):
    # empty string cell will be read as null cell
    convert_options = csv.ConvertOptions(strings_can_be_null=True)
    arrow_table = csv.read_csv(csv_pth, convert_options=convert_options)
    return arrow_table.to_batches()[0]


# TODO: add test utility for table-valued parameter / default value
