from encodings import utf_8
from numpy import int64
import pyarrow as pa
import json
from sql_metadata import Parser
from stonewave.sql.udtfs.base_function import BaseFunction, udtf
import re

STRING_LIST_TYPE = pa.list_(pa.utf8())


def _prefix_table_name(table_name, column_name):
    return "{}.{}".format(table_name, column_name)


def _try_with_default_value(obj, property, default_value):
    try:
        return getattr(obj, property)
    except Exception as e:
        return default_value


def _is_single_table_without_cte(tables, with_queries):
    return len(tables) == 1 and not with_queries


def _pre_process_sql(sql):
    return sql.replace("?", "1")


def _dedup_and_fix_tables(tables):
    tables = sorted(set(tables))
    # sql-metadata doesn't parse `FROM (WITH cte (...))` correctly
    for t in tables:
        if "WITH" == t.upper():
            tables.remove(t)
    return tables


def _parse_query(sql):
    sql = _pre_process_sql(sql)
    parser = Parser(sql)
    query_type = _try_with_default_value(parser, "query_type", "unknown")
    tables = _dedup_and_fix_tables(_try_with_default_value(parser, "tables", []))
    with_queries = _try_with_default_value(parser, "with_queries", {})
    sub_queries = _try_with_default_value(parser, "subqueries", {})
    columns = _try_with_default_value(parser, "columns", [])
    table_alias = _try_with_default_value(parser, "tables_aliases", {})

    if _is_single_table_without_cte(tables, with_queries):
        columns = [_prefix_table_name(tables[0], c) if "." not in c else c for c in columns]

    for _, query in with_queries.items():
        columns_in_cte, _, _ = _parse_query(query)
        columns += columns_in_cte

    for _, query in sub_queries.items():
        columns_in_sub_query, _, _ = _parse_query(query)
        columns += columns_in_sub_query

    return (columns, tables, query_type)


def _is_table_function(sql, table):
    return f"{table}(" in sql


# TODO: sql-metadata doesn't support table function yet,
# https://github.com/macbre/sql-metadata/issues/276
# here is a hacky approach by replacing `my_func()` with `my_func`
def _pre_process_table_function(sql):
    parser = Parser(sql)
    tables = _dedup_and_fix_tables(_try_with_default_value(parser, "tables", []))
    for table in tables:
        if _is_table_function(sql, table):
            pattern = re.compile(f"{table}\\((.*?)\\)")
            sql = re.sub(pattern, table, sql)

    return sql


@udtf(is_parser=True)
class ParseSqlFunction(BaseFunction):
    def __init__(self):
        pass

    def get_name(self):
        return "parse_sql"

    def process(self, params, table_writer, context):
        sql = params[0]
        sql = _pre_process_table_function(sql)
        columns, tables, query_type = _parse_query(sql)

        columns = sorted(set(columns))
        table_writer.write_column("columns", STRING_LIST_TYPE, [columns])
        table_writer.write_column("tables", STRING_LIST_TYPE, [tables])
        table_writer.write_column("query_type", pa.utf8(), [query_type])
