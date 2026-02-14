import streamlit as st
import sys
import os

# Ensure the project root is in sys.path for absolute imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ui.api_client import ApiClient
from ui.styles import apply_custom_styles
from ui.views.home import render_home
from ui.views.candidates import render_candidates
from ui.views.rag import render_rag
from ui.views.indexes import render_indexes

# Configuration - Could be moved to a config file in the future
from app.core.config import API_URL


# Page Configuration
st.set_page_config(
    page_title="HR Tech AI", 
    page_icon="🤖",
    layout="wide"
)

# Apply Global Design System Styles
apply_custom_styles()

st.title("HR Tech AI Platform")

# Session State Initialization for Navigation
if "menu_selection" not in st.session_state:
    st.session_state.menu_selection = "Home"

# Sidebar Navigation
with st.sidebar:
    st.markdown("### HR Tech AI")


    menu = st.selectbox(
        "Menu Principal",
        ["Home", "Candidatos", "Query / RAG", "Gestão de Índices"],
        key="menu_selection"
    )

# Singleton-like API Client in Session State
if "api_client" not in st.session_state:
    st.session_state.api_client = ApiClient(base_url=API_URL)

client = st.session_state.api_client

# Route rendering based on selection
if menu == "Home":
    render_home(client)
elif menu == "Candidatos":
    render_candidates(client)
elif menu == "Query / RAG":
    render_rag(client)
elif menu == "Gestão de Índices":
    render_indexes(client)

# Persistent Footer
st.markdown('<div class="footer">Plataforma Inteligente de Recrutamento</div>', unsafe_allow_html=True)
