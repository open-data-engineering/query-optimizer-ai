from sqlglot import parse_one


def parse_sql(sql: str):
    return parse_one(sql)


def extract_features(sql_ast):
    return {
        "has_select_star": "*" in str(sql_ast).lower(),
        "has_order_by": "order by" in str(sql_ast).lower(),
        "has_limit": "limit" in str(sql_ast).lower(),
    }
