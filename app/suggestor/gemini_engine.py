import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("models/gemini-1.5-pro-002")


def generate_suggestions_gemini(query: str, schemas: dict = None) -> list:
    schema_str = ""
    if schemas:
        for table, fields in schemas.items():
            field_str = "\n".join(
                [
                    f"- `{col['name']}`: {col['type']}"
                    for col in fields
                    if "error" not in col
                ]
            )
            schema_str += f"\n### Esquema da tabela `{table}`:\n{field_str}\n"

    prompt = f"""
        Você é um especialista em SQL e otimização de queries para BigQuery.

        Dada a seguinte query SQL:

        ```sql
        {query}
        {schema_str}
        ```

        Gere sugestões de otimização no formato JSON:

        [
        {{
        “title”: “Título da sugestão”,
        “description”: “Descrição explicando o porquê da sugestão”,
        “suggested_fix”: “Exemplo de nova versão da query ou trecho”,
        “impact_percent”: 30.0
        }}
        ]

        Retorne apenas o JSON, sem explicações extras.
    """

    response = model.generate_content(prompt)
    content = response.text.strip()

    content = content.strip("```json").strip("```").strip()

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
