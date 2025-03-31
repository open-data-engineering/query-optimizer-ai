from sqlglot import parse_one
from sqlglot.errors import ParseError
from app.core.utils import sanitize_bigquery_identifiers


def parse_sql(sql: str):
    sanitized_sql = sanitize_bigquery_identifiers(sql)
    try:
        return parse_one(sanitized_sql), None
    except ParseError as e:
        return None, str(e)
