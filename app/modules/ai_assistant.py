import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import html
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "ai_engine")
    )
)

from sql_agent import (
    generate_sql,
    run_query,
    generate_insight
)

def render_chart(df, chart_type="auto"):
    """Renders interactive Plotly charts with dark cyber theme."""
    if df.empty:
        st.info("No rows returned for visualization.")
        return

    cols = df.columns.tolist()
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "string", "category"]).columns.tolist()

    if not cat_cols:
        cat_cols = [cols[0]]
    if not num_cols:
        st.dataframe(df, use_container_width=True)
        return

    x_col = cat_cols[0]
    y_col = num_cols[0]

    st.subheader("📈 Interactive Visualization")

    selected_chart = st.radio(
        "Select Visual Representation:",
        ["📊 Bar Chart", "📈 Line Chart", "🍩 Donut/Pie Chart", "📍 Scatter Plot", "📋 Data Table Only"],
        horizontal=True,
        key=f"chart_selector_{len(df)}"
    )

    if "Bar" in selected_chart:
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            color=y_col if len(df) <= 15 else None,
            color_continuous_scale="Viridis" if len(df) <= 15 else None,
            title=f"{y_col} by {x_col}",
            template="plotly_dark"
        )
        fig.update_layout(
            paper_bgcolor="rgba(15, 23, 42, 0.8)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=40, b=20),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    elif "Line" in selected_chart:
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            markers=True,
            title=f"{y_col} Trend",
            template="plotly_dark"
        )
        fig.update_traces(line=dict(color="#06B6D4", width=3), marker=dict(size=8, color="#10B981"))
        fig.update_layout(
            paper_bgcolor="rgba(15, 23, 42, 0.8)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=40, b=20),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    elif "Donut" in selected_chart or "Pie" in selected_chart:
        fig = px.pie(
            df,
            names=x_col,
            values=y_col,
            hole=0.4,
            title=f"{y_col} Distribution",
            template="plotly_dark"
        )
        fig.update_layout(
            paper_bgcolor="rgba(15, 23, 42, 0.8)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=40, b=20),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    elif "Scatter" in selected_chart:
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            size=y_col if (df[y_col] > 0).all() else None,
            color=x_col,
            title=f"{y_col} vs {x_col}",
            template="plotly_dark"
        )
        fig.update_layout(
            paper_bgcolor="rgba(15, 23, 42, 0.8)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=40, b=20),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

def show():
    st.markdown(
        """
        <div class="hero-banner">
            <div class="hero-title">🤖 AI Intelligence Copilot</div>
            <div class="hero-subtitle">
                Ask business questions in natural language. Powered by <b>Google Gemini 2.5 Flash</b>, your query is transformed into optimized SQL, executed instantly, and synthesized into executive business recommendations.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if "ai_history" not in st.session_state:
        st.session_state.ai_history = []

    # Prompt Suggestions Chips
    st.markdown("<b style='color:#FFFFFF; font-size:1.15rem;'>💡 Popular Question Templates (Click to insert):</b>", unsafe_allow_html=True)
    
    sample_queries = [
        "🔥 Top 5 products by sales",
        "📈 Sales and profit by region",
        "📦 Products where stock is less than reorder level",
        "💳 Total sales by payment mode",
        "👥 Top 10 customers by total spend"
    ]

    cols = st.columns(len(sample_queries))
    selected_prompt = None
    for i, q in enumerate(sample_queries):
        if cols[i].button(q, key=f"chip_{i}", use_container_width=True):
            selected_prompt = q

    default_value = selected_prompt if selected_prompt else ""

    with st.form(key="ai_query_form"):
        question = st.text_input(
            "Enter your business question:",
            value=default_value,
            placeholder="e.g. What are the top 5 selling product categories by profit?"
        )
        submit_button = st.form_submit_button("🚀 Generate SQL & Run Intelligence", use_container_width=True)

    if submit_button or selected_prompt:
        target_question = question if question.strip() else selected_prompt
        
        if not target_question or not target_question.strip():
            st.warning("Please enter or select a business question.")
            return

        start_time = time.time()
        
        try:
            with st.spinner("🧠 AI generating SQL query..."):
                sql = generate_sql(target_question)

            # Bulletproof HTML SQL Display Block
            escaped_sql = html.escape(sql)
            st.markdown(
                f"""
                <div style="background-color: #0F172A; border: 2px solid #06B6D4; border-radius: 14px; padding: 20px; margin-top: 20px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
                    <div style="color: #06B6D4; font-weight: 800; font-size: 1.05rem; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 12px;">📝 GENERATED SQL QUERY</div>
                    <div style="background-color: #030712; border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 10px; padding: 18px; color: #38BDF8 !important; -webkit-text-fill-color: #38BDF8 !important; font-family: 'Fira Code', 'Courier New', monospace; font-size: 1.25rem !important; font-weight: 700 !important; line-height: 1.6; white-space: pre-wrap; word-break: break-word;">{escaped_sql}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            with st.spinner("⚡ Executing query against database..."):
                df = run_query(sql)

            elapsed = time.time() - start_time
            
            st.markdown(
                f"""
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:24px; margin-bottom:12px;">
                    <h3 style="margin:0; color:#FFFFFF; font-size:1.4rem;">📊 Query Results ({len(df)} rows)</h3>
                    <span class="status-badge status-badge-mysql">⏱ Execution Time: {elapsed:.2f}s</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.dataframe(df, use_container_width=True)

            # Download CSV
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Export Result set as CSV",
                data=csv,
                file_name="retail_ai_query_result.csv",
                mime="text/csv"
            )

            # Visualization
            if not df.empty:
                render_chart(df)

            # AI Insight
            with st.spinner("💡 Synthesizing executive business insights..."):
                insight = generate_insight(target_question, df)

            st.markdown(
                f"""
                <div class="insight-card">
                    <h3 style="color:#06B6D4; margin-top:0;">💡 Executive AI Insight & Action Plan</h3>
                    <div style="color:#CBD5E1; line-height:1.7; font-size:1.05rem;">
                        {insight}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Store in session state history
            st.session_state.ai_history.insert(0, {
                "question": target_question,
                "sql": sql,
                "rows": len(df),
                "insight": insight
            })

        except Exception as e:
            st.error(f"Execution Error: {e}")

    # History Drawer
    if st.session_state.ai_history:
        st.markdown("<br><hr>", unsafe_allow_html=True)
        st.subheader("📜 Recent Copilot Query History")
        
        for idx, item in enumerate(st.session_state.ai_history[:5]):
            with st.expander(f"🔍 Question {idx+1}: {item['question']} ({item['rows']} rows)"):
                st.code(item['sql'], language="sql")
                st.markdown(item['insight'])