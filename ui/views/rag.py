import streamlit as st
from ui.api_client import ApiClient

def render_rag(client: ApiClient):
    st.header("Consulta Inteligente (RAG)")
    q_rag = st.text_input("Faça uma pergunta ao sistema sobre os candidatos")
    
    if st.button("Perguntar"):
        if q_rag:
            with st.spinner("Gerando resposta..."):
                try:
                    r = client.rag_query(q_rag)
                    answer = r.get("answer", "Sem resposta.")
                    st.success("Resposta Gerada:")
                    st.markdown(f"> {answer}")
                except Exception as e:
                    st.error(f"Erro: {e}")
        else:
            st.warning("Digite uma pergunta.")
