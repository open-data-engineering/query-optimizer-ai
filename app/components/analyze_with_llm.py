from app.suggestor.openai_engine import generate_suggestions_openai
from app.suggestor.gemini_engine import generate_suggestions_gemini


# def analyze_query_with_llm(query, schemas, llm_provider):
# if llm_provider == "OpenAI (GPT-4)":
#     return generate_suggestions_openai(query, schemas=schemas)
# return generate_suggestions_gemini(query, schemas=schemas)


def analyze_query_with_llm(query, schemas, llm_provider="LLaMA"):
    if llm_provider == "OpenAI":
        return generate_suggestions_openai(query, schemas=schemas)
    else:
        return generate_suggestions_gemini(query, schemas=schemas)
