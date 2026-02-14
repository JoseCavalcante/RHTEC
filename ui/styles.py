import streamlit as st

def apply_custom_styles():
    st.markdown("""
<style>
    /* Custom CSS for Dialogs & Layout */
    
    /* Force button size to be smaller/compact */
    .stButton, .stButton button, .stButton button p {
        font-size: 12px !important;
        height: auto !important;
        padding-top: 2px !important;
        padding-bottom: 2px !important;
        min-height: 0px !important;
        margin-top: 0px !important;
        margin-bottom: 0px !important;
    }
    /* Style tertiary buttons as links */
    .stButton button[kind="tertiary"], .stButton button[kind="tertiary"] p {
        color: white !important;
        font-size: 12px !important;
        text-decoration: none !important;
        border: none !important;
        background: transparent !important;
        padding: 0px !important;
        margin: 0px !important;
        font-weight: normal !important;
        justify-content: flex-start !important;
    }
    .stButton button[kind="tertiary"]:hover {
        text-decoration: underline !important;
        color: #f0f0f0 !important;
    }
    .stButton button[kind="tertiary"]:focus:not(:active) {
        border-color: transparent !important;
        color: white !important;
    }
    /* Reduce spacing between columns in horizontal block */
    [data-testid="stHorizontalBlock"] {
        gap: 0.25rem !important;
        align-items: center !important;
        margin-top: 0px !important;
        margin-bottom: 0px !important;
        padding-top: 0px !important;
        padding-bottom: 0px !important;
    }
    /* Eliminate vertical spacing for dividers */
    hr {
        margin-top: 0px !important;
        margin-bottom: 0px !important;
        padding-top: 0px !important;
        padding-bottom: 0px !important;
        border: 0;
        border-top: 1px solid #eee !important;
    }
    /* Reduce padding in vertical block */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    /* Compact markdown paragraphs */
    div[data-testid="stMarkdownContainer"] p {
        margin-bottom: 0px !important;
        line-height: 1.4 !important;
    }
    /* Reduce vertical gap between elements inside columns */
    div[data-testid="column"] > div {
        gap: 0px !important;
        align-items: center !important;
    }
    /* Titles/Headers Size & Spacing */
    h1 {
        font-size: 26px !important;
        padding-top: 0.2rem !important;
        padding-bottom: 0px !important;
        margin-bottom: 0px !important;
    }
    h3 {
        font-size: 20px !important;
        padding-top: 0.2rem !important;
        padding-bottom: 0.2rem !important;
        margin-bottom: 0.4rem !important;
    }
    /* Specific sidebar title spacing */
    [data-testid="stSidebar"] h3 {
        margin-bottom: 0.8rem !important;
    }
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {
        margin-bottom: 0.8rem !important;
        font-size: 14px !important;
    }
    /* Footer styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(255, 255, 255, 0.05); /* Fundo sutil para destaque */
        color: #cadbee; /* Cor de destaque */
        text-align: center;
        padding: 8px 0;
        font-size: 14px;
        font-weight: 600;
        z-index: 1000;
        pointer-events: none;
        backdrop-filter: blur(5px); /* Efeito de desfoque moderno */
    }
</style>
""", unsafe_allow_html=True)
