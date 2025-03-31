import streamlit as st


def render_metrics_summary(metrics: dict):
    total_queries = metrics.get("total_queries", 0)
    total_processed_gb = metrics.get("total_processed_gb", 0.0)
    avg_duration = metrics.get("avg_duration", 0.0)
    total_cost = metrics.get("total_cost", 0.0)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("⚠️ Queries Pesadas", total_queries)
    col2.metric("📦 TB Processados", f"{total_processed_gb:.2f} TB")
    col3.metric("⏱️ Duração Média", f"{avg_duration:.2f} s")
    col4.metric("💸 Custo Total", f"{total_cost:.2f} USD")
