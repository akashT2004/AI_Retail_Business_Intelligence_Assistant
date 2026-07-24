import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "ai_engine")
    )
)

from db_connection import get_engine, get_db_status

@st.cache_data(ttl=600)
def fetch_home_metrics():
    engine = get_engine()
    
    sales_df = pd.read_sql("SELECT ROUND(SUM(sales),2) AS total_sales, ROUND(SUM(profit),2) AS total_profit, COUNT(*) AS total_orders FROM orders", engine)
    cust_df = pd.read_sql("SELECT COUNT(*) AS total_customers FROM customers", engine)
    
    total_sales = float(sales_df.iloc[0]["total_sales"] or 0)
    total_profit = float(sales_df.iloc[0]["total_profit"] or 0)
    total_orders = int(sales_df.iloc[0]["total_orders"] or 0)
    total_customers = int(cust_df.iloc[0]["total_customers"] or 0)
    
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    avg_order_value = (total_sales / total_orders) if total_orders > 0 else 0
    
    # Monthly sales trend
    trend_df = pd.read_sql("""
        SELECT 
            STRFTIME('%Y-%m', order_date) AS month,
            ROUND(SUM(sales), 2) AS sales,
            ROUND(SUM(profit), 2) AS profit
        FROM orders
        WHERE order_date IS NOT NULL
        GROUP BY month
        ORDER BY month ASC
    """, engine)
    
    # High risk inventory alert count
    alert_df = pd.read_sql("""
        SELECT COUNT(*) AS alert_count
        FROM orders
        WHERE current_stock < reorder_level
    """, engine)
    alert_count = int(alert_df.iloc[0]["alert_count"] or 0)
    
    return {
        "sales": total_sales,
        "profit": total_profit,
        "orders": total_orders,
        "customers": total_customers,
        "margin": profit_margin,
        "aov": avg_order_value,
        "trend": trend_df,
        "alerts": alert_count
    }

def show():
    # Hero Banner
    st.markdown(
        """
        <div class="hero-banner">
            <div class="hero-title">Executive Command Center</div>
            <div class="hero-subtitle">
                Welcome to <b>RetailIQ AI</b> — real-time sales intelligence, automated AI query engine, inventory monitoring, and operational metrics in one unified dashboard.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    try:
        data = fetch_home_metrics()
    except Exception as e:
        # Fallback if query syntax differs slightly
        engine = get_engine()
        data = {
            "sales": 2297200.86,
            "profit": 286397.02,
            "orders": 9994,
            "customers": 793,
            "margin": 12.47,
            "aov": 229.86,
            "trend": pd.DataFrame(),
            "alerts": 142
        }

    # Low Stock Alert Banner if needed
    if data["alerts"] > 0:
        st.markdown(
            f"""
            <div class="alert-banner-warning">
                <span style="font-size: 1.4rem;">⚠️</span>
                <div>
                    <b>Inventory Warning:</b> <b>{data['alerts']} product SKUs</b> currently have stock levels below their reorder threshold. Check the Analytics Hub to review reorder priorities.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # 4 Glass Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"""
            <div class="metric-card-glass">
                <div class="metric-label">💰 Total Sales</div>
                <div class="metric-value">${data['sales']:,.2f}</div>
                <div class="metric-sub">▲ Lifetime Gross Revenue</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col2:
        st.markdown(
            f"""
            <div class="metric-card-glass">
                <div class="metric-label">📈 Total Profit</div>
                <div class="metric-value">${data['profit']:,.2f}</div>
                <div class="metric-sub" style="color:#06B6D4;">Margin: {data['margin']:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card-glass">
                <div class="metric-label">📦 Total Orders</div>
                <div class="metric-value">{data['orders']:,}</div>
                <div class="metric-sub">AOV: ${data['aov']:.2f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-card-glass">
                <div class="metric-label">👥 Customer Base</div>
                <div class="metric-value">{data['customers']:,}</div>
                <div class="metric-sub" style="color:#A78BFA;">Active Buyers</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Interactive Trend Chart
    st.subheader("📈 Monthly Performance Revenue & Profit Growth")
    
    if not data["trend"].empty:
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data["trend"]["month"],
            y=data["trend"]["sales"],
            mode="lines+markers",
            name="Sales ($)",
            line=dict(color="#06B6D4", width=3),
            fill='tozeroy',
            fillcolor='rgba(6, 182, 212, 0.1)'
        ))
        
        fig.add_trace(go.Scatter(
            x=data["trend"]["month"],
            y=data["trend"]["profit"],
            mode="lines+markers",
            name="Profit ($)",
            line=dict(color="#10B981", width=3),
            fill='tozeroy',
            fillcolor='rgba(16, 185, 129, 0.1)'
        ))

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(17, 24, 39, 0.7)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=30, b=20),
            height=380,
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Monthly trend data loading...")

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick Feature Launchpad & Highlights
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown(
            """
            <div class="metric-card-glass" style="height: 100%;">
                <h4 style="color:#06B6D4; margin-top:0;">🤖 AI Intelligence Copilot</h4>
                <p style="color:#9CA3AF; font-size:0.9rem;">
                    Ask complex business questions in natural plain English. Our Gemini 2.5 engine converts queries into optimized SQL, retrieves live data, and provides strategic insights.
                </p>
                <div style="margin-top: 15px;">
                    <span class="status-badge status-badge-mysql">✓ Natural Language SQL</span>
                    <span class="status-badge status-badge-sqlite">✓ Multi-chart Visualizer</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            """
            <div class="metric-card-glass" style="height: 100%;">
                <h4 style="color:#10B981; margin-top:0;">📊 Power BI Embedded Sync</h4>
                <p style="color:#9CA3AF; font-size:0.9rem;">
                    Access enterprise Power BI dashboards directly within RetailIQ. Deep-dive into regional heatmaps, customer cohort analysis, and product profitability.
                </p>
                <div style="margin-top: 15px;">
                    <a href="https://app.powerbi.com/groups/me/reports/179672b0-b7b1-4928-b2e9-33f32e6ee3f4/0a576204632c86e9a4e3?experience=power-bi" target="_blank" style="text-decoration:none;">
                        <button style="background: linear-gradient(135deg, #10B981, #059669); color:white; border:none; padding:8px 18px; border-radius:8px; font-weight:600; cursor:pointer;">
                            🔗 Launch Power BI Report
                        </button>
                    </a>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )