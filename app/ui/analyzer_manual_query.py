import sqlparse
import streamlit as st
from app.components.suggestion_card import render_suggestion_card
from app.components.table_schema import render_table_schemas
from app.components.header import render_page_header
from app.components.analyze_with_llm import analyze_query_with_llm

from app.core.utils import (
    get_table_schema,
    extract_table_names_from_query,
    estimate_query_cost,
)


def render_manual_query_analyzer():
    render_page_header("🧠 Query Optimizer AI", "🔎 Análise Manual de Queries")

    user_query = st.text_area(
        "Cole sua Query SQL abaixo:",
        height=200,
        placeholder="Ex: SELECT * FROM sales ORDER BY date",
    )

    if st.button("🔍 Analisar com IA"):
        if not user_query.strip():
            st.warning("⚠️ Por favor, cole uma query válida.")
            return

        st.session_state.suggestions_cache = {}

        query = user_query.strip()
        table_names = extract_table_names_from_query(query)
        schemas = {t: get_table_schema(t) for t in table_names}

        st.session_state.query = query
        st.session_state.schemas = schemas

        query_cost, bytes_processed = estimate_query_cost(query)
        st.session_state.query_cost = float(query_cost)
        st.session_state.query_bytes = bytes_processed

        llm_provider = "LLaMA"

        st.session_state.suggestions = analyze_query_with_llm(
            query, schemas, llm_provider
        )
        st.session_state.show_suggestions = True

    if st.session_state.get("show_suggestions"):
        __extracted_from_render_manual_query_analyzer__(st)


def __extracted_from_render_manual_query_analyzer__(st):
    st.subheader("🔍 Query Original")

    try:
        formatted_query = sqlparse.format(
            st.session_state.query.strip(), reindent=True, keyword_case="upper"
        )
    except Exception:
        formatted_query = st.session_state.query

    st.code(formatted_query, language="sql")

    render_table_schemas(st.session_state.schemas)

    st.subheader("💡 Sugestões de Otimização")

    for i, suggestion in enumerate(st.session_state.suggestions):
        key_prefix = f"suggestion_{i}"
        render_suggestion_card(
            index=i,
            suggestion=suggestion,
            query_cost=st.session_state.query_cost,
            key_prefix=key_prefix,
        )
