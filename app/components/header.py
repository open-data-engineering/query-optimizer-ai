import streamlit as st


def render_page_header(title: str, subtitle: str):
    st.title(title)
    st.markdown("  \n" * 4)
    st.subheader(subtitle)
