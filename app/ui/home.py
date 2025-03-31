import streamlit as st
from app.auth.sso_google import get_login_url, exchange_code_for_token, get_user_info
from app.components.header import render_page_header


def render_home():
    render_page_header("🧠 Query Optimizer AI", "🔎  Otimize suas Queries SQL com IA")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "code" in st.query_params and not st.session_state.authenticated:
        code = st.query_params["code"]
        token_response = exchange_code_for_token(code)
        if access_token := token_response.get("access_token"):
            user_info = get_user_info(access_token)
            st.session_state.authenticated = True
            st.session_state.user_name = user_info.get("name")
            st.session_state.user_email = user_info.get("email")
            st.session_state.db_type = "BigQuery"
            st.success(f"🔐 Autenticado como {st.session_state.user_name}")
            st.rerun()
        else:
            st.error("❌ Erro ao autenticar com o Google.")
            return

    if not st.session_state.authenticated:
        login_url = get_login_url()

        st.markdown(
            f"""
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 70vh;">
                <h3 style="text-align: center;">👋 Faça login com sua conta Google para continuar:</h3>
                <a href="{login_url}" target="_self">
                    <img src="https://developers.google.com/identity/images/btn_google_signin_dark_normal_web.png" alt="Login com Google" width="240">
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    st.success(
        f"✅ Bem-vindo, {st.session_state.user_name} ({st.session_state.user_email})"
    )

    st.markdown("💾 Banco detectado automaticamente: `BigQuery`")

    if st.button("✅ Acessar o sistema"):
        if not st.session_state.db_type:
            st.warning("⚠️ Escolha um tipo de banco.")
        else:
            st.rerun()
