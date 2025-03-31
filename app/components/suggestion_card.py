import sqlparse
import streamlit as st
from app.core.utils import estimate_query_cost, execute_query_with_limit


def render_suggestion_card(index, suggestion, query_cost, key_prefix):
    raw_sql = suggestion.get("suggested_fix", "").strip()
    try:
        formatted_sql = sqlparse.format(raw_sql, reindent=True, keyword_case="upper")
    except Exception:
        formatted_sql = raw_sql

    with st.expander(f"Sugestão #{index + 1}: {suggestion['title']}"):
        st.write(suggestion["description"])
        st.code(formatted_sql, language="sql")

        impact_percent = suggestion.get("impact_percent", 0.0)
        try:
            saving = round((impact_percent / 100) * query_cost, 2)
        except Exception:
            saving = 0.0
        percent_display = f"{impact_percent:.1f}%"

        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Economia Estimada", f"{saving} USD", delta=percent_display)
        col2.metric("💸 Custo Real", f"{query_cost} USD")
        col3.metric(
            "📦 Processado",
            f"{st.session_state.get('suggestions_cache', {}).get(key_prefix, {}).get('bytes', 0) / 1e9:.2f} GB",
        )

        if saving > query_cost:
            st.caption(
                "⚠️ A economia estimada é maior que o custo real. Interprete com cautela."
            )

        run_button_disabled = (
            not raw_sql
            or raw_sql.upper() in ("N/A", "NA")
            or not raw_sql.lower().startswith("select")
        )

        if st.button(
            "⚡ Executar sugestão (dry run)",
            key=f"{key_prefix}_run",
            disabled=run_button_disabled,
        ):
            try:
                cost, bytes_processed = estimate_query_cost(raw_sql)
                rows = execute_query_with_limit(raw_sql, limit=10, sample_percent=10.0)

                if "suggestions_cache" not in st.session_state:
                    st.session_state.suggestions_cache = {}

                st.session_state.suggestions_cache[key_prefix] = {
                    "cost": cost,
                    "bytes": bytes_processed,
                    "rows": rows,
                }
                st.success("✅ Execução simulada concluída.")
            except Exception as e:
                st.error(f"❌ Erro ao executar dry run: {e}")

        if key_prefix in st.session_state.get("suggestions_cache", {}):
            result = st.session_state.suggestions_cache[key_prefix]
            st.caption(
                f"💸 **Custo estimado:** {result['cost']:.2f} USD — "
                f"📦 **Processado:** {result['bytes'] / 1e9:.2f} GB"
            )
            if result.get("rows"):
                st.markdown("📋 **Registros retornados:**")
                st.dataframe(result["rows"])
