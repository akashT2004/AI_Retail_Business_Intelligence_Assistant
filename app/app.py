import streamlit as st
import sys
import os

# Add root directory and modules to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ai_engine")))

from modules.custom_css import apply_custom_css
from db_connection import get_db_status

st.set_page_config(
    page_title="RetailIQ AI | Business Intelligence Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Global Design System
apply_custom_css()

# Sidebar Header & Brand
st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 10px 0 20px 0;">
        <div style="font-size: 2.2rem; margin-bottom: 4px;">⚡ <b>RetailIQ</b> <span style="color:#06B6D4;">AI</span></div>
        <div style="font-size: 0.82rem; color: #9CA3AF; font-weight: 500;">Next-Gen Business Intelligence</div>
    </div>
    """,
    unsafe_allow_html=True
)

# System Health & Status Indicator
db_status = get_db_status()
if db_status.get("type") == "mysql":
    status_html = """
    <div style="margin-bottom: 24px; padding: 10px 14px; background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 12px; font-size: 0.8rem; color: #34D399; display: flex; align-items: center; gap: 8px;">
        <span style="font-size: 1rem;">🟢</span> <b>MySQL Engine Active</b>
    </div>
    """
else:
    status_html = """
    <div style="margin-bottom: 24px; padding: 10px 14px; background: rgba(245, 158, 11, 0.12); border: 1px solid rgba(245, 158, 11, 0.25); border-radius: 12px; font-size: 0.8rem; color: #FBBF24; display: flex; align-items: center; gap: 8px;">
        <span style="font-size: 1rem;">⚡</span> <b>SQLite / CSV Fallback Engine</b>
    </div>
    """
st.sidebar.markdown(status_html, unsafe_allow_html=True)

# Navigation Radio
page = st.sidebar.radio(
    "Navigation Menu",
    [
        "🏠 Executive Command Center",
        "🤖 AI Intelligence Copilot",
        "📈 Interactive Analytics Hub",
        "📊 Power BI Dashboard",
        "ℹ Diagnostic & System Specs"
    ],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style="font-size: 0.78rem; color: #6B7280; text-align: center; margin-top: 20px;">
        RetailIQ AI v2.5 Executive Edition<br>
        Powered by Gemini 2.5 & Plotly
    </div>
    """,
    unsafe_allow_html=True
)

# Route Pages
if page == "🏠 Executive Command Center":
    from modules.home import show
    show()

elif page == "🤖 AI Intelligence Copilot":
    from modules.ai_assistant import show
    show()

elif page == "📈 Interactive Analytics Hub":
    from modules.analytics import show
    show()

elif page == "📊 Power BI Dashboard":
    from modules.dashboard import show
    show()

elif page == "ℹ Diagnostic & System Specs":
    from modules.about import show
    show()