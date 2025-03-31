import streamlit as st


def render_llm_selector(key=None):
    return st.selectbox(
        "🧠 Modelo de IA", ["OpenAI (GPT-4)", "Gemini (Google)"], key=key
    )
