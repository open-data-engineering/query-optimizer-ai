import re
from google.cloud import bigquery


def extract_table_names_from_query(query: str) -> list:
    """
    Extrai nomes de tabelas no formato projeto.dataset.tabela (com ou sem crase).
    Ignora INFORMATION_SCHEMA.
    """
    pattern = r"`?([\w\-]+)\.([\w]+)\.([\w]+)`?"
    matches = re.findall(pattern, query)
    return [
        f"{p}.{d}.{t}" for p, d, t in matches if "information_schema" not in t.lower()
    ]


def clean_sql(sql: str):
    return sql.strip()


def sanitize_bigquery_identifiers(sql: str) -> str:
    """
    Coloca crases em identificadores BigQuery com hífen para evitar erro no parse.
    Exemplo:
    yams-lab-nonprod.dataset.table → `yams-lab-nonprod.dataset.table`
    """
    pattern = r"\b([\w-]+)\.([\w]+)\.([\w]+)\b"
    matches = re.findall(pattern, sql)

    for project, dataset, table in matches:
        if "-" in project:
            full_name = f"{project}.{dataset}.{table}"
            sql = sql.replace(full_name, f"`{full_name}`")

    return sql


def get_table_schema(table_id: str) -> list:
    """
    Retorna o schema de uma tabela no formato:
    [ {"name": "coluna", "type": "STRING"}, ... ]
    """
    client = bigquery.Client()
    try:
        table = client.get_table(table_id)
        return [
            {"name": field.name, "type": field.field_type} for field in table.schema
        ]
    except Exception as e:
        return [{"error": f"Erro ao buscar schema de {table_id}: {e}"}]


def estimate_query_cost(sql: str, location: str = "US") -> tuple:
    client = bigquery.Client(location=location)
    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)

    try:
        query_job = client.query(sql, job_config=job_config)
        bytes_processed = query_job.total_bytes_processed
        tb_processed = bytes_processed / (1024**4)
        cost = round(tb_processed * 5.0, 2)
        return cost, bytes_processed
    except Exception:
        return 0.0, 0


def dry_run_query(query: str) -> dict:
    client = bigquery.Client()
    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
    query_job = client.query(query, job_config=job_config)

    return {
        "bytes_processed": query_job.total_bytes_processed,
        "estimated_cost": round(
            query_job.total_bytes_processed / 1_000_000_000 * 5.0, 4
        ),
    }


def execute_query_with_limit(query: str, limit: int = 10, sample_percent: float = None):
    """
    Executa a query com um LIMIT adicional, e opcionalmente aplica TABLESAMPLE SYSTEM.

    Args:
        query (str): A query SQL original.
        limit (int): Número de linhas retornadas.
        sample_percent (float, optional): Percentual para TABLESAMPLE SYSTEM (1 a 100).

    Returns:
        list[dict]: Resultados como dicionários.
    """
    client = bigquery.Client()

    cleaned_query = query.strip().rstrip(";")

    if sample_percent and sample_percent > 0 and sample_percent <= 100:
        if match := re.match(
            r"SELECT\s+(.*?)\s+FROM\s+`?([\w\-.]+)`?",
            cleaned_query,
            re.IGNORECASE | re.DOTALL,
        ):
            projection = match[1]
            table = match[2]
            sampled_query = f"""
            SELECT {projection}
            FROM `{table}`
            TABLESAMPLE SYSTEM ({sample_percent} PERCENT)
            LIMIT {limit}
            """
        else:
            sampled_query = f"SELECT * FROM ({cleaned_query}) LIMIT {limit}"
    else:
        sampled_query = f"SELECT * FROM ({cleaned_query}) LIMIT {limit}"

    job = client.query(sampled_query)
    results = job.result()
    return [dict(row.items()) for row in results]
