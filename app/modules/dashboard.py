import streamlit as st

POWERBI_URL = "https://app.powerbi.com/groups/me/reports/179672b0-b7b1-4928-b2e9-33f32e6ee3f4/0a576204632c86e9a4e3?experience=power-bi"

def show():
    st.markdown(
        """
        <div class="hero-banner">
            <div class="hero-title">📊 Executive Power BI Dashboard</div>
            <div class="hero-subtitle">
                Access your interactive enterprise reports published directly on Power BI Cloud Service.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown(
            """
            <div class="metric-card-glass" style="margin-bottom: 20px;">
                <h3 style="color:#06B6D4; margin-top:0;">🌐 Power BI Service Report</h3>
                <p style="color:#9CA3AF; line-height:1.6;">
                    The Power BI dashboard provides interactive cross-filtering for gross profit margins, regional sales maps, customer retention matrix, and inventory turnover schedules.
                </p>
                <div style="margin-top:20px;">
                    <a href="https://app.powerbi.com/groups/me/reports/179672b0-b7b1-4928-b2e9-33f32e6ee3f4/0a576204632c86e9a4e3?experience=power-bi" target="_blank" style="text-decoration:none;">
                        <button style="background: linear-gradient(135deg, #06B6D4 0%, #2563EB 100%); color:white; border:none; padding:12px 28px; border-radius:10px; font-weight:700; cursor:pointer; font-size:1rem; box-shadow: 0 4px 15px rgba(6,182,212,0.3);">
                            🚀 Launch Power BI Report in New Window ↗
                        </button>
                    </a>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            """
            <div class="metric-card-glass">
                <h4 style="color:#10B981; margin-top:0;">⚡ Live Integration Features</h4>
                <ul style="color:#9CA3AF; font-size:0.88rem; line-height:1.8; padding-left:20px;">
                    <li>Direct MySQL Data Model Connection</li>
                    <li>Automatic Scheduled Refresh</li>
                    <li>Cross-visual Drillthrough</li>
                    <li>Mobile View Ready</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )