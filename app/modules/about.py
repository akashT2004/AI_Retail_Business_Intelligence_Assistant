import streamlit as st
import sys
import os
import pandas as pd

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "ai_engine")
    )
)

from db_connection import get_db_status, get_engine
from sql_agent import DATABASE_SCHEMA

def show():
    st.markdown(
        """
        <div class="hero-banner">
            <div class="hero-title">ℹ Diagnostic & System Specifications</div>
            <div class="hero-subtitle">
                System architecture details, database engine health, active AI LLM model configuration, and database table schemas.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    db_status = get_db_status()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card-glass">
                <div class="metric-label">🗄️ Database Engine Status</div>
                <div style="font-size:1.1rem; font-weight:700; color:#FFFFFF; margin-top:5px;">
                    {db_status.get('type','unknown').upper()}
                </div>
                <div style="font-size:0.82rem; color:#9CA3AF; margin-top:4px;">
                    {db_status.get('message','-')}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            """
            <div class="metric-card-glass">
                <div class="metric-label">🧠 AI Engine LLM</div>
                <div style="font-size:1.1rem; font-weight:700; color:#FFFFFF; margin-top:5px;">
                    Google Gemini 2.5 Flash
                </div>
                <div style="font-size:0.82rem; color:#10B981; margin-top:4px;">
                    ✓ SQL Agent & Business Insights Active
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            """
            <div class="metric-card-glass">
                <div class="metric-label">💻 Application Runtime</div>
                <div style="font-size:1.1rem; font-weight:700; color:#FFFFFF; margin-top:5px;">
                    Python & Streamlit
                </div>
                <div style="font-size:0.82rem; color:#A78BFA; margin-top:4px;">
                    ✓ Plotly Cyber Theme Active
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Schema Explorer
    st.subheader("📋 Active Database Schema Explorer")
    
    tab_schema, tab_tech = st.tabs(["🗂️ Database Schema", "🛠️ Technology Stack"])

    with tab_schema:
        st.code(DATABASE_SCHEMA, language="text")
        
        try:
            engine = get_engine()
            st.subheader("🔍 Sample Tables Inspector")
            table_select = st.selectbox("Inspect Table:", ["orders", "customers", "products"])
            sample_df = pd.read_sql(f"SELECT * FROM {table_select} LIMIT 5", engine)
            st.dataframe(sample_df, use_container_width=True)
        except Exception as e:
            st.warning(f"Unable to inspect sample table: {e}")

    with tab_tech:
        st.markdown(
            """
            - **Frontend Framework**: Streamlit with Custom Glassmorphism CSS Design System
            - **AI Engine**: Google Gemini 2.5 Flash Generative AI via `google-generativeai` & LangChain
            - **Data Visualization**: Plotly Express & Plotly Graph Objects (Interactive Dark Mode)
            - **Database Layer**: Dual-Engine (MySQL Engine + In-Memory SQLite Fallback from CSV)
            - **Data Processing**: Pandas & SQLAlchemy
            - **BI Integration**: Power BI Service Cloud Embedded
            """
        )