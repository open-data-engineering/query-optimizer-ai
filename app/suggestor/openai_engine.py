import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_suggestions_openai(query: str, schemas: dict = None) -> list:
    schema_text = ""
    if schemas:
        schema_text = "\n\n".join(
            f"Schema da tabela `{table}`:\n"
            + "\n".join(
                [
                    f"- {col['name']}: {col['type']}"
                    for col in cols
                    if "error" not in col
                ]
            )
            for table, cols in schemas.items()
        )

    prompt = f"""
        Você é um especialista em SQL para BigQuery.

        Abaixo está uma query para ser analisada:
        ```sql
        {query}
        ```

        {schema_text if schema_text else ""}

        Com base nisso, gere sugestões de otimização no seguinte formato JSON:

        [
        {{
            "title": "Título da sugestão",
            "description": "Descrição explicando o porquê",
            "suggested_fix": "Nova versão da query ou trecho",
            "impact_percent": 20.0,
            "estimated_saving": 5.0
        }}
        ]

        Retorne **apenas o JSON**.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Você é um especialista em otimização de SQL para BigQuery.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return [
            {
                "title": "Sugestão da IA",
                "description": content,
                "suggested_fix": query,
                "impact_percent": 0.0,
            }
        ]
