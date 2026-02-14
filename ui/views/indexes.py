import streamlit as st
import pandas as pd
import re
from ui.api_client import ApiClient

def render_indexes(client: ApiClient):
    """
    UI for managing Pinecone vector indexes.
    Allows listing, creating, and viewing details of indexes.
    """
    st.header("Gerenciamento do Pinecone")
    
    tab_list, tab_create, tab_detail = st.tabs(["Listar Índices", "Criar Índice", "Detalhes"])
    
    with tab_list:
        if st.button("Atualizar Lista"):
            try:
                data = client.list_indexes()
                
                # Normalize data to a list
                indexes_list = []
                if isinstance(data, dict):
                    if 'indexes' in data:
                        indexes_list = data['indexes']
                    else:
                        # Try to find any list in the dict values or just treat dict as single record
                        indexes_list = [data]
                elif isinstance(data, list):
                    indexes_list = data
                
                if indexes_list:
                    df = pd.DataFrame(indexes_list)
                    st.dataframe(df)
                else:
                    st.info("Nenhum índice encontrado.")
            except Exception as e:
                st.error(f"Erro ao listar índices: {e}")
                
    with tab_create:
        new_index_name = st.text_input("Nome do Novo Índice", help="Apenas letras minúsculas, números e hífens (-)")
        if st.button("Criar Índice"):
            if new_index_name:
                if not re.match(r'^[a-z0-9-]+$', new_index_name):
                    st.error("O nome deve conter apenas letras minúsculas, números e hífens (-).")
                else:
                    with st.spinner(f"Criando índice '{new_index_name}'..."):
                        try:
                            # O endpoint espera query param 'name_index'
                            client.create_index(new_index_name)
                            st.success(f"Índice '{new_index_name}' criado!")
                        except Exception as e:
                            st.error(f"Erro ao criar: {e}")
            else:
                st.warning("Informe um nome para o índice.")

    with tab_detail:
        detail_name = st.text_input("Nome do Índice para Detalhes")
        if st.button("Ver Detalhes"):
            if detail_name:
                try:
                    details = client.get_index_detail(detail_name)
                    
                    # Extract main info
                    # Structure varies slightly by Pinecone version, handle gracefully
                    index_name = details.get('name', detail_name)
                    dimension = details.get('dimension', 'N/A')
                    metric = details.get('metric', 'N/A')
                    status = details.get('status', {})
                    state = status.get('state', 'Unknown')
                    is_ready = status.get('ready', False)
                    host = details.get('host', '')
                    spec = details.get('spec', {})
                    
                    # Display nicely
                    st.subheader(f"📌 {index_name}")
                    
                    # Metrics Row
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.metric("Dimensão", dimension)
                    with c2:
                        st.metric("Métrica", metric)
                    with c3:
                        st.metric("Estado", state, delta="Ready" if is_ready else "Not Ready")
                        
                    st.divider()
                    
                    # Host Info
                    if host:
                        st.write(f"**Host:** `{host}`")
                        
                    # Cloud / Spec Info
                    if spec:
                        st.markdown("### Infraestrutura")
                        serverless = spec.get('serverless')
                        pod = spec.get('pod')
                        
                        if serverless:
                            st.info(f"☁️ Serverless - {serverless.get('cloud', '').upper()} ({serverless.get('region', '')})")
                        elif pod:
                            st.info(f"📦 Pod - {pod.get('environment', '')} ({pod.get('pod_type', '')})")
                            
                    # Raw Data Toggle
                    with st.expander("Ver JSON Bruto"):
                        st.json(details)
                        
                except Exception as e:
                    st.error(f"Erro ao obter detalhes: {e}")
