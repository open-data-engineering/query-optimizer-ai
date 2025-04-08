import streamlit as st
from app.collectors.bigquery_jobs import collect_jobs
from app.parser.performance_analyzer import flag_heavy_queries
from app.core.utils import extract_table_names_from_query, get_table_schema
from app.components.metrics_summary import render_metrics_summary
from app.components.header import render_page_header
from app.components.table_schema import render_table_schemas
from app.components.suggestion_card import render_suggestion_card
from app.components.analyze_with_llm import analyze_query_with_llm


def render_historical_query_analyzer():
    render_page_header("🧠 Query Optimizer AI", "🔎 Análise Histórica de Queries")

    period = st.selectbox(
        "Selecione o período de análise:",
        [7, 14, 30, 60],
        index=2,
        format_func=lambda x: f"Últimos {x} dias",
    )

    if st.button("📊 Buscar Queries Pesadas"):
        df = collect_jobs(period)
        st.session_state.heavy_df = flag_heavy_queries(df)

    if st.session_state.get("heavy_df") is not None:
        __render_analysis_dashboard__(st.session_state.heavy_df)


def __render_analysis_dashboard__(heavy_df):
    st.subheader("📈 Métricas Gerais")

    filtered_df = heavy_df[
        ~heavy_df["query"].str.upper().str.contains("INFORMATION_SCHEMA")
    ].copy()

    filtered_df["cost_usd"] = filtered_df.apply(
        lambda row: row.get("cost_usd") or round(row["tb_processed"] * 5.0, 2), axis=1
    )

    heavy_df_sorted = filtered_df.sort_values(by="cost_usd", ascending=False)

    if heavy_df_sorted.empty:
        st.warning("⚠️ Nenhuma query pesada encontrada para o período selecionado.")
        return

    render_metrics_summary(
        {
            "total_queries": len(heavy_df_sorted),
            "total_processed_gb": round(heavy_df_sorted["tb_processed"].sum(), 2),
            "avg_duration": round(heavy_df_sorted["duration_seconds"].mean(), 2),
            "total_cost": round(heavy_df_sorted["cost_usd"].sum(), 2),
        }
    )

    st.subheader("❗ Queries Pesadas Detectadas")

    for i, (_, row) in enumerate(heavy_df_sorted.iterrows(), start=1):
        __render_query_analysis_block__(i, row)


def __render_query_analysis_block__(index, row):
    query = row["query"]
    query_cost = row["cost_usd"]
    suggestion_key = f"suggestion_{index}"
    show_key = f"show_suggestion_{index}"

    st.markdown(f"### 🔹 Query #{index}")
    st.code(query, language="sql")
    st.caption(f"💰 Custo real da consulta: **{query_cost} USD**")

    if show_key not in st.session_state:
        st.session_state[show_key] = False

    if st.button(f"🔍 Analisar com IA para Query #{index}", key=f"llm_button_{index}"):
        st.session_state[show_key] = True

    if st.session_state[show_key]:
        with st.spinner("Consultando a IA..."):
            try:
                __analyze_and_render_suggestions__(query, suggestion_key, query_cost)
            except Exception as e:
                st.error(f"❌ Erro ao consultar a IA: {e}")

    st.divider()


def __analyze_and_render_suggestions__(query, suggestion_key, query_cost):
    table_names = extract_table_names_from_query(query)
    schemas = {t: get_table_schema(t) for t in table_names}

    render_table_schemas(schemas)

    if suggestion_key not in st.session_state:
        st.session_state[suggestion_key] = analyze_query_with_llm(
            query, schemas, "LLaMA"
        )

    st.subheader("💡 Sugestões geradas pela IA:")

    for j, suggestion in enumerate(st.session_state[suggestion_key]):
        key_prefix = f"{suggestion_key}_{j}"
        render_suggestion_card(j, suggestion, query_cost, key_prefix)
