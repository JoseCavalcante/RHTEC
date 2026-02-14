import streamlit as st
import time
from ui.api_client import ApiClient

# --- Dialogs & Helper Functions ---

@st.dialog("Detalhes do Candidato")
def show_candidate_details(cand):
    """Displays full candidate details in a modal."""
    metadata = cand.get('metadata', {})
    c_name = metadata.get('name', 'Sem Nome')
    c_seniority = metadata.get('seniority', 'N/A')
    c_skills = metadata.get('skills', [])
    
    st.markdown(f"### 👤 {c_name}")
    st.caption(f"Senioridade: {c_seniority}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Experiência", f"{metadata.get('experience_years', 0)} anos")
    with col2:
        st.metric("Score", f"{cand.get('score', 0):.2f}")
    
    st.divider()
    st.markdown("#### 🛠️ Habilidades")
    st.write(", ".join(c_skills) if c_skills else "-")
    
    st.markdown("#### 📝 Resumo")
    st.text_area("Currículo", metadata.get('text', ''), height=200, disabled=True)

@st.dialog("Editar Candidato")
def edit_candidate_dialog(client: ApiClient, cand_id: str, current_meta: dict):
    """Modal for editing candidate information."""
    with st.form("edit_candidate_form"):
        new_name = st.text_input("Nome", value=current_meta.get('name', ''))
        
        # Handling Seniority Selectbox Index
        seniority_options = ["Estagiário", "Júnior", "Pleno", "Sênior", "Especialista"]
        current_sen = current_meta.get('seniority', 'Pleno')
        sen_index = seniority_options.index(current_sen) if current_sen in seniority_options else 2
        new_seniority = st.selectbox("Senioridade", seniority_options, index=sen_index)
        
        new_exp = st.number_input("Anos de Experiência", min_value=0, value=int(float(current_meta.get('experience_years', 0))), step=1)
        
        current_skills = current_meta.get('skills', [])
        skills_str = ", ".join(current_skills) if isinstance(current_skills, list) else str(current_skills)
            
        new_skills = st.text_area("Habilidades (separadas por vírgula)", value=skills_str)
        new_text = st.text_area("Texto do Currículo", value=current_meta.get('text', ''), height=200)
        
        if st.form_submit_button("Salvar Alterações", use_container_width=True):
            updated_payload = {
                "name": new_name,
                "skills": [s.strip() for s in new_skills.split(",") if s.strip()],
                "seniority": new_seniority,
                "experience_years": new_exp,
                "text": new_text
            }
            
            try:
                with st.spinner("Atualizando..."):
                    client.update_candidate(cand_id, updated_payload)
                    st.toast("Candidato atualizado com sucesso!", icon="✅")
                    # Invalidate cache
                    if 'candidates_list' in st.session_state:
                        del st.session_state.candidates_list
                    st.rerun()
            except Exception as e:
                st.error(f"Erro ao atualizar: {e}")

@st.dialog("Confirmar Exclusão")
def confirm_delete_dialog(client: ApiClient, id_to_del: str, name_to_del: str):
    """Modal for deletion confirmation."""
    st.markdown("""
        <style>
            [data-testid="stDialogCloseButton"], 
            button[aria-label="Close"], 
            .stDialogCloseButton,
            div[role="dialog"] button:has(svg[viewBox="0 0 24 24"]) {
                display: none !important;
                visibility: hidden !important;
                opacity: 0 !important;
                pointer-events: none !important;
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown(f"<div style='margin-bottom: 25px;'>Tem certeza que deseja excluir <b>{name_to_del}</b>?</div>", unsafe_allow_html=True)
    c_sim, c_nao = st.columns(2)
    with c_sim:
        if st.button("SIM", use_container_width=True, key="btn_conf_del"):
            try:
                client.delete_candidate(id_to_del)
                st.toast(f"Candidato removido!", icon="🗑️")
                # Invalidate cache
                if 'candidates_list' in st.session_state:
                    del st.session_state.candidates_list
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao excluir: {e}")
    with c_nao:
        if st.button("NÃO", use_container_width=True, key="btn_cancel_del"):
            st.rerun()

# --- Main Render Function ---

def render_candidates(client: ApiClient):
    st.header("Gestão de Candidatos")
    
    # Navigation logic for Candidatos
    if "candidatos_tab" not in st.session_state:
        st.session_state.candidatos_tab = "Buscar"
    
    selected_tab = st.radio(
        "Navegação Candidatos", 
        ["Buscar", "Adicionar Currículo", "Listar Todos"],
        horizontal=True,
        label_visibility="collapsed",
        key="candidatos_tab"
    )
    
    # --- Tab: Buscar ---
    if selected_tab == "Buscar":
        q = st.text_input("Descreva o perfil desejado")
        if st.button("Buscar"):
            if q:
                try:
                    results = client.search_candidates(q)
                    st.session_state.search_results = results
                except Exception as e:
                    st.error(f"Erro: {e}")
            else:
                st.warning("Digite uma busca.")
        
        if 'search_results' in st.session_state:
            results = st.session_state.search_results
            if not results:
                st.warning("⚠️ Nenhum candidato encontrado para este perfil.")
            else:
                st.write(f"Encontrados: {len(results)}")
                
                for item in results:
                    metadata = item.get('metadata', {})
                    name = metadata.get('name', 'Candidato')
                    score = item.get('score', 0)
                    skills = metadata.get('skills', [])
                    seniority = metadata.get('seniority', 'N/A')
                    experience = metadata.get('experience_years', 0)
                    text = metadata.get('text', '')
                    
                    with st.expander(f"{name} - Score: {score:.2f}"):
                        st.write(f"**Skills:** {', '.join(skills)}")
                        st.write(f"**Seniority:** {seniority}")
                        st.write(f"**Experience:** {experience} anos")
                        st.text_area("Resumo", text, height=100, key=f"summary_{item.get('id')}")

    # --- Tab: Adicionar ---
    elif selected_tab == "Adicionar Currículo":
        st.markdown("### Cadastro de Novo Talento")
        
        t_manual, t_upload = st.tabs(["Manual", "Upload de Arquivos 📂"])
        
        with t_manual:
            with st.form("add_resume_form", clear_on_submit=True):
                st.markdown("#### Dados Pessoais")
                name = st.text_input("Nome Completo", placeholder="Ex: Ana Silva")
                
                st.markdown("#### Perfil Profissional")
                col1, col2 = st.columns(2)
                with col1:
                    seniority = st.selectbox("Senioridade", ["Estagiário", "Júnior", "Pleno", "Sênior", "Especialista"])
                with col2:
                    experience_years = st.number_input("Anos de Experiência", min_value=0, step=1)
                
                st.markdown("#### Competências & Currículo")
                skills_input = st.text_area("Habilidades (separadas por vírgula)")
                text = st.text_area("Texto Completo do Currículo", height=200)
                
                submitted = st.form_submit_button("Salvar Candidato")
                
                if submitted:
                    if not name or not text:
                        st.warning("⚠️ Nome e Texto do Currículo são obrigatórios!")
                    else:
                        skills_list = [s.strip() for s in skills_input.split(",") if s.strip()]
                        payload = {
                            "name": name,
                            "skills": skills_list,
                            "seniority": seniority,
                            "experience_years": experience_years,
                            "text": text
                        }
                        
                        try:
                            with st.spinner("Processando..."):
                                client.add_resume(payload)
                                st.success(f"✅ Candidato **{name}** adicionado!")
                                if 'candidates_list' in st.session_state:
                                    del st.session_state.candidates_list
                        except Exception as e:
                            st.error(f"❌ Erro ao adicionar: {e}")

        with t_upload:
            st.markdown("*Extração automática de dados via IA (PDF/DOCX).*")
            st.write("") 
            uploaded_files = st.file_uploader("Selecione currículos", accept_multiple_files=True, type=['pdf', 'docx'])
            
            if st.button("Processar Arquivos"):
                if not uploaded_files:
                    warning_placeholder = st.empty()
                    warning_placeholder.warning("⚠️ Selecione pelo menos um arquivo.")
                    time.sleep(3)
                    warning_placeholder.empty()
                else:
                    total = len(uploaded_files)
                    progress_bar = st.progress(0)
                    success_count = 0
                    
                    try:
                        files_payload = [('files', (f.name, f.getvalue(), f.type)) for f in uploaded_files]
                        with st.spinner(f"Processando {total} arquivos..."):
                             results = client.upload_resumes(files_payload)
                            
                        for i, res in enumerate(results):
                            progress_bar.progress((i + 1) / total)
                            if res.get('status') == 'success':
                                success_count += 1
                        
                        st.success(f"Concluído! {success_count}/{total} arquivos importados.")
                        if success_count > 0 and 'candidates_list' in st.session_state:
                                del st.session_state.candidates_list
                    except Exception as e:
                        st.error(f"Erro: {e}")

    # --- Tab: Listar Todos ---
    elif selected_tab == "Listar Todos":
        if 'candidates_list' not in st.session_state:
             with st.spinner("Carregando lista..."):
                try:
                    candidates = client.get_all_candidates()
                    st.session_state.candidates_list = candidates
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao carregar: {e}")
        
        if 'candidates_list' in st.session_state:
            candidates = st.session_state.candidates_list
            
            @st.fragment
            def render_candidate_interface():
                # Search term state
                if 'active_search_term' not in st.session_state:
                    st.session_state.active_search_term = ''
                if 'expander_reset_id' not in st.session_state:
                    st.session_state.expander_reset_id = 0

                # Top Header: Total and Search
                col_total, col_search = st.columns([1, 2], vertical_alignment="center")
                with col_total:
                    st.write(f"**Total de Candidato:** {len(candidates)}")
                
                with col_search:
                    with st.expander(f"Pesquisar{'\u200b' * st.session_state.expander_reset_id}"):
                        temp_search = st.text_input("Digite o nome", value=st.session_state.active_search_term, key="temp_search_input")
                        c_apply, c_cancel, _ = st.columns([0.7, 1.0, 5], gap="small")
                        if c_apply.button("OK", use_container_width=True):
                            st.session_state.active_search_term = temp_search
                            st.rerun()
                        if c_cancel.button("Sair", use_container_width=True):
                            st.session_state.active_search_term = ''
                            st.session_state.expander_reset_id += 1
                            st.rerun()

                # Filter and Sort
                search_query = st.session_state.active_search_term
                filtered = sorted(candidates, key=lambda x: x.get('metadata', {}).get('name', '').lower())
                if search_query:
                    filtered = [c for c in filtered if c.get('metadata', {}).get('name', '').lower().startswith(search_query.lower())]

                # Table Header
                c1, c2, c3, c4, c5 = st.columns([1, 2, 1, 1, 2], vertical_alignment="center")
                c1.markdown("**ID**")
                c2.markdown("**Nome**")
                c3.markdown("**Exp.**")
                c4.markdown("**Nível**")
                c5.markdown("**Ações**")
                st.divider()

                # Rows
                for cand in filtered:
                    meta = cand.get('metadata', {})
                    c_id = cand.get('id', 'N/A')
                    col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 1, 2], vertical_alignment="center")
                    col1.text(c_id[:8])
                    col2.text(meta.get('name', 'Sem Nome'))
                    col3.text(f"{meta.get('experience_years', 0)} anos")
                    col4.text(meta.get('seniority', 'N/A'))
                    
                    with col5:
                        b2, b3, _ = st.columns([0.5, 0.5, 2], gap="small")
                        if b2.button("Editar", key=f"ed_{c_id}", type="tertiary"):
                            edit_candidate_dialog(client, c_id, meta)
                        if b3.button("Excluir", key=f"del_{c_id}", type="tertiary"):
                            confirm_delete_dialog(client, c_id, meta.get('name', ''))
                    st.divider()

            render_candidate_interface()
