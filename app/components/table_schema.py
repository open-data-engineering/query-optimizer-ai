import streamlit as st


def render_table_schemas(schemas: dict):
    for table, fields in schemas.items():
        with st.expander(f"📄 Esquema da Tabela: {table}"):
            for col in fields:
                if "error" in col:
                    st.error(col["error"])
                else:
                    st.markdown(f"- `{col['name']}`: {col['type']}")
