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

from db_connection import get_engine

@st.cache_data(ttl=600)
def load_base_data():
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM orders", engine)
    return df

def show():
    st.markdown(
        """
        <div class="hero-banner">
            <div class="hero-title">📈 Interactive Analytics Hub</div>
            <div class="hero-subtitle">
                Comprehensive business intelligence suite. Filter across dates, regions, categories, and customer segments to explore profitability, product performance, and warehouse logistics.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    try:
        raw_df = load_base_data()
    except Exception as e:
        st.error(f"Failed to load analytics dataset: {e}")
        return

    if raw_df.empty:
        st.warning("No data found in orders database.")
        return

    # Interactive Filters Bar
    st.markdown("### 🎛 Global Interactive Filters")
    
    f1, f2, f3 = st.columns(3)
    
    with f1:
        regions = ["All Regions"] + sorted(list(raw_df["region"].dropna().unique()))
        selected_region = st.selectbox("📍 Region Filter:", regions)

    with f2:
        categories = ["All Categories"] + sorted(list(raw_df["category"].dropna().unique()))
        selected_category = st.selectbox("📦 Category Filter:", categories)

    with f3:
        segments = ["All Segments"] + sorted(list(raw_df["segment"].dropna().unique()))
        selected_segment = st.selectbox("👥 Customer Segment:", segments)

    # Filter Logic
    df = raw_df.copy()
    if selected_region != "All Regions":
        df = df[df["region"] == selected_region]
    if selected_category != "All Categories":
        df = df[df["category"] == selected_category]
    if selected_segment != "All Segments":
        df = df[df["segment"] == selected_segment]

    st.markdown(f"**Showing {len(df):,} filtered order records out of {len(raw_df):,} total.**")
    st.markdown("<br>", unsafe_allow_html=True)

    # 4 Analytics Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "💰 Sales & Financials",
        "🏷️ Product & Category Intelligence",
        "🚚 Customer & Operations",
        "📦 Inventory & Warehouse Health"
    ])

    # ---------------- TAB 1: FINANCIALS ----------------
    with tab1:
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("Regional Sales & Profit")
            reg_df = df.groupby("region")[["sales", "profit"]].sum().reset_index()
            fig = px.bar(
                reg_df,
                x="region",
                y=["sales", "profit"],
                barmode="group",
                color_discrete_sequence=["#06B6D4", "#10B981"],
                template="plotly_dark",
                labels={"value": "USD ($)", "variable": "Metric"}
            )
            fig.update_layout(
                paper_bgcolor="rgba(17, 24, 39, 0.7)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=380
            )
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.subheader("Revenue Share by Category")
            cat_df = df.groupby("category")["sales"].sum().reset_index()
            fig = px.pie(
                cat_df,
                names="category",
                values="sales",
                hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Pastel,
                template="plotly_dark"
            )
            fig.update_layout(
                paper_bgcolor="rgba(17, 24, 39, 0.7)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=380
            )
            st.plotly_chart(fig, use_container_width=True)

        # State Sales Map / Table
        st.subheader("State-by-State Revenue & Profit Distribution")
        state_df = df.groupby("state")[["sales", "profit", "quantity"]].sum().reset_index().sort_values(by="sales", ascending=False)
        st.dataframe(state_df, use_container_width=True)

    # ---------------- TAB 2: PRODUCTS ----------------
    with tab2:
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("🔥 Top 10 Most Profitable Products")
            top_p = df.groupby("product_name")["profit"].sum().reset_index().sort_values(by="profit", ascending=False).head(10)
            fig = px.bar(
                top_p,
                y="product_name",
                x="profit",
                orientation="h",
                color="profit",
                color_continuous_scale="Viridis",
                template="plotly_dark"
            )
            fig.update_layout(
                paper_bgcolor="rgba(17, 24, 39, 0.7)",
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(autorange="reversed"),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.subheader("⚠️ Top 10 Least Profitable / Loss Products")
            bot_p = df.groupby("product_name")["profit"].sum().reset_index().sort_values(by="profit", ascending=True).head(10)
            fig = px.bar(
                bot_p,
                y="product_name",
                x="profit",
                orientation="h",
                color="profit",
                color_continuous_scale="Reds_r",
                template="plotly_dark"
            )
            fig.update_layout(
                paper_bgcolor="rgba(17, 24, 39, 0.7)",
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(autorange="reversed"),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Sub-Category Performance Breakdown")
        sub_df = df.groupby("sub_category")[["sales", "profit"]].sum().reset_index().sort_values(by="sales", ascending=False)
        fig = px.bar(
            sub_df,
            x="sub_category",
            y="sales",
            color="profit",
            title="Sales & Profitability by Sub-Category",
            template="plotly_dark"
        )
        fig.update_layout(
            paper_bgcolor="rgba(17, 24, 39, 0.7)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=380
        )
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- TAB 3: CUSTOMER & OPERATIONS ----------------
    with tab3:
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Sales Volume by Shipping Mode")
            ship_df = df.groupby("ship_mode")[["sales", "profit"]].sum().reset_index()
            fig = px.bar(
                ship_df,
                x="ship_mode",
                y="sales",
                color="ship_mode",
                template="plotly_dark"
            )
            fig.update_layout(
                paper_bgcolor="rgba(17, 24, 39, 0.7)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=380
            )
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.subheader("Customer Segment Revenue Contribution")
            seg_df = df.groupby("segment")["sales"].sum().reset_index()
            fig = px.pie(
                seg_df,
                names="segment",
                values="sales",
                hole=0.4,
                template="plotly_dark"
            )
            fig.update_layout(
                paper_bgcolor="rgba(17, 24, 39, 0.7)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=380
            )
            st.plotly_chart(fig, use_container_width=True)

        if "payment_mode" in df.columns:
            st.subheader("Payment Mode Breakdown")
            pay_df = df.groupby("payment_mode")["sales"].sum().reset_index()
            fig = px.bar(pay_df, x="payment_mode", y="sales", color="payment_mode", template="plotly_dark")
            fig.update_layout(paper_bgcolor="rgba(17, 24, 39, 0.7)", plot_bgcolor="rgba(0,0,0,0)", height=350)
            st.plotly_chart(fig, use_container_width=True)

    # ---------------- TAB 4: INVENTORY ----------------
    with tab4:
        st.subheader("📦 Inventory Reorder Priority Monitor")
        
        inv_df = df[["product_name", "category", "warehouse", "current_stock", "reorder_level", "lead_time_days"]].drop_duplicates()
        inv_df["reorder_needed"] = inv_df["current_stock"] < inv_df["reorder_level"]
        
        low_stock_items = inv_df[inv_df["reorder_needed"]].copy()
        
        st.markdown(
            f"""
            <div class="alert-banner-warning">
                <span style="font-size:1.5rem;">🚨</span>
                <div>
                    <b>Inventory Warning:</b> Found <b>{len(low_stock_items)} items</b> where stock level is BELOW reorder point!
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.subheader("Low Stock Reorder List")
        st.dataframe(low_stock_items, use_container_width=True)

        if "warehouse" in df.columns and "lead_time_days" in df.columns:
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Stock Distribution by Warehouse")
                w_df = df.groupby("warehouse")["current_stock"].sum().reset_index()
                fig = px.pie(w_df, names="warehouse", values="current_stock", template="plotly_dark")
                fig.update_layout(paper_bgcolor="rgba(17, 24, 39, 0.7)", plot_bgcolor="rgba(0,0,0,0)", height=350)
                st.plotly_chart(fig, use_container_width=True)

            with c2:
                st.subheader("Average Lead Time (Days) by Warehouse")
                l_df = df.groupby("warehouse")["lead_time_days"].mean().reset_index()
                fig = px.bar(l_df, x="warehouse", y="lead_time_days", color="warehouse", template="plotly_dark")
                fig.update_layout(paper_bgcolor="rgba(17, 24, 39, 0.7)", plot_bgcolor="rgba(0,0,0,0)", height=350)
                st.plotly_chart(fig, use_container_width=True)