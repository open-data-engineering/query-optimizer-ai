import streamlit as st
from app.ui.home import render_home
from app.ui.analyzer_manual_query import render_manual_query_analyzer
from app.ui.analyzer_historical_query import render_historical_query_analyzer

st.set_page_config(page_title="Query Optimizer AI", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

st.session_state.setdefault("db_type", None)
st.session_state.setdefault("user_name", "Usuário")
st.session_state.setdefault("user_email", None)
st.session_state.setdefault("selected_dashboard", "manual")

if st.session_state.authenticated and st.session_state.db_type is None:
    st.session_state.db_type = "BigQuery"

if not st.session_state.authenticated:
    render_home()
else:
    st.sidebar.markdown(f"**{st.session_state.user_name}**")

    db_type = st.session_state.get("db_type", "❌ Não selecionado")
    # db_icon = {
    #     "BigQuery": "🔵",
    #     "PostgreSQL": "🟢",
    #     "Snowflake": "❄️",
    #     "DuckDB": "🦆",
    #     None: "⚠️",
    # }.get(db_type, "💾")

    # st.sidebar.markdown(f"{db_icon} Banco: `{db_type}`")
    st.sidebar.markdown(f"Banco: `{db_type}`")

    st.sidebar.markdown("---")
    st.sidebar.title("Navegação")

    st.sidebar.markdown("  \n")

    if st.sidebar.button("Análise Manual"):
        st.session_state.selected_dashboard = "manual"

    if st.sidebar.button("Análise Histórica"):
        st.session_state.selected_dashboard = "bigquery"

    if st.session_state.selected_dashboard == "manual":
        render_manual_query_analyzer()
    elif st.session_state.selected_dashboard == "bigquery":
        render_historical_query_analyzer()
