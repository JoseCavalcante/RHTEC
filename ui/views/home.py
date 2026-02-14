import streamlit as st
from ui.api_client import ApiClient

def render_home(client: ApiClient):
    st.header("Bem-vindo ao HR Tech AI")
    st.write("Verificando status da API...")
    try:
        # Health check
        r = client.health_check()
        if r.get("status") == "running":            
            st.metric(label="Status", value="Online", delta="OK")
        else:
            st.error(f"Erro na API: {r}")
    except Exception as e:
        st.error(f"Falha na conexão: {e}")
