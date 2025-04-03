from google.cloud import bigquery
from google.auth.exceptions import DefaultCredentialsError


def collect_jobs(last_days: int = 30, max_results: int = 1000):
    try:
        client = bigquery.Client()

        query = f"""
          SELECT
            query,
            user_email,
            total_bytes_processed / 1e9 AS tb_processed,
            total_slot_ms / 1000 AS slot_seconds,
            TIMESTAMP_DIFF(end_time, start_time, SECOND) AS duration_seconds,
            start_time,
            end_time
          FROM
            region-us.INFORMATION_SCHEMA.JOBS_BY_PROJECT
          WHERE
            job_type = 'QUERY'
            AND creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {last_days} DAY)
            AND state = 'DONE'
            AND query IS NOT NULL
          LIMIT {max_results}
        """
        return client.query(query).to_dataframe()

    except DefaultCredentialsError as e:
        print("❌ Credenciais não configuradas corretamente:", e)
    except Exception as e:
        print("❌ Erro ao executar a query:", e)
        raise
