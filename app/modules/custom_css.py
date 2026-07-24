import streamlit as st

def apply_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=Fira+Code:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: #F3F4F6;
        }

        /* Main App Background */
        .stApp {
            background-color: #0B0F19 !important;
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(6, 182, 212, 0.15) 0px, transparent 50%),
                radial-gradient(at 50% 50%, rgba(16, 185, 129, 0.05) 0px, transparent 60%) !important;
            background-attachment: fixed !important;
        }

        /* Sidebar Container */
        section[data-testid="stSidebar"] {
            background-color: #0F172A !important;
            border-right: 1px solid rgba(255, 255, 255, 0.12) !important;
        }

        /* Radio Buttons Label & Text - FORCE BRIGHT WHITE (20px font) */
        section[data-testid="stSidebar"] [data-testid="stRadio"] *,
        section[data-testid="stSidebar"] [data-testid="stRadio"] label,
        section[data-testid="stSidebar"] [data-testid="stRadio"] p,
        section[data-testid="stSidebar"] [data-testid="stRadio"] span,
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        div[data-testid="stRadio"] label,
        div[data-testid="stRadio"] label p,
        div[data-testid="stRadio"] label span,
        div[data-testid="stRadio"] p,
        div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            font-size: 1.2rem !important;
            font-weight: 800 !important;
            opacity: 1 !important;
        }

        div[data-testid="stRadio"] div[role="radiogroup"] label {
            padding: 12px 16px !important;
            border-radius: 12px !important;
            margin-bottom: 8px !important;
            background: rgba(255, 255, 255, 0.04) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            transition: all 0.2s ease !important;
        }

        div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
            background: rgba(6, 182, 212, 0.25) !important;
            border-color: #06B6D4 !important;
        }

        /* Active Radio Button Highlight */
        div[data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"],
        div[data-testid="stRadio"] div[role="radiogroup"] label[aria-checked="true"] {
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.35) 0%, rgba(37, 99, 235, 0.35) 100%) !important;
            border: 2px solid #06B6D4 !important;
            box-shadow: 0 4px 15px rgba(6, 182, 212, 0.4) !important;
        }

        div[data-testid="stRadio"] div[role="radiogroup"] label[aria-checked="true"] p,
        div[data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"] p {
            color: #38BDF8 !important;
            -webkit-text-fill-color: #38BDF8 !important;
            font-weight: 800 !important;
        }

        /* Input Fields (Text inputs) */
        .stTextInput input {
            background-color: #1E293B !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            font-size: 1.15rem !important;
            font-weight: 600 !important;
            border: 1.5px solid rgba(6, 182, 212, 0.5) !important;
            border-radius: 12px !important;
            padding: 12px 16px !important;
        }

        .stTextInput input::placeholder {
            color: #94A3B8 !important;
            -webkit-text-fill-color: #94A3B8 !important;
        }

        .stTextInput label, .stSelectbox label {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            font-size: 1.15rem !important;
            font-weight: 700 !important;
        }

        /* ABSOLUTE OVERRIDE FOR CODE BLOCKS - REMOVE ALL WHITE HIGHLIGHT BOXES */
        code, pre, div[data-testid="stCodeBlock"], div[data-testid="stCodeBlock"] *, code *, pre *, span.code-line, span.hljs-keyword, span.hljs-string, span.hljs-title, span.hljs-number {
            background-color: #030712 !important;
            background: #030712 !important;
            color: #38BDF8 !important;
            -webkit-text-fill-color: #38BDF8 !important;
            font-size: 1.2rem !important;
            font-family: 'Fira Code', 'Courier New', monospace !important;
            line-height: 1.6 !important;
            box-shadow: none !important;
        }

        div[data-testid="stCodeBlock"] {
            border: 2px solid #06B6D4 !important;
            border-radius: 14px !important;
            padding: 16px !important;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.6) !important;
        }

        /* Glassmorphic Cards */
        .metric-card-glass {
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 16px;
            padding: 22px;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.6);
            transition: all 0.3s ease;
        }
        
        .metric-card-glass:hover {
            transform: translateY(-4px);
            border-color: #06B6D4;
        }

        .metric-label {
            font-size: 0.9rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #94A3B8;
            margin-bottom: 6px;
        }

        .metric-value {
            font-size: 2rem;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 4px;
        }

        .metric-sub {
            font-size: 0.85rem;
            font-weight: 600;
            color: #34D399;
        }

        /* Status Badges */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 700;
        }

        .status-badge-mysql {
            background: rgba(16, 185, 129, 0.2);
            color: #34D399;
            border: 1px solid rgba(16, 185, 129, 0.4);
        }

        .status-badge-sqlite {
            background: rgba(245, 158, 11, 0.2);
            color: #FBBF24;
            border: 1px solid rgba(245, 158, 11, 0.4);
        }

        /* Hero Banner */
        .hero-banner {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.9) 100%);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 20px;
            padding: 30px 34px;
            margin-bottom: 26px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.4);
        }

        .hero-title {
            font-size: 2.4rem;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 8px;
        }

        .hero-subtitle {
            font-size: 1.1rem;
            color: #CBD5E1;
            line-height: 1.6;
        }

        /* Insight Callout Card */
        .insight-card {
            background: rgba(15, 23, 42, 0.95);
            border-left: 6px solid #06B6D4;
            border-radius: 14px;
            padding: 26px;
            margin-top: 26px;
            box-shadow: 0 12px 30px rgba(0,0,0,0.5);
        }

        /* Custom Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: rgba(15, 23, 42, 0.9);
            padding: 6px;
            border-radius: 14px;
            border: 1px solid rgba(255, 255, 255, 0.12);
        }

        .stTabs [data-baseweb="tab"] {
            height: 48px;
            border-radius: 10px;
            color: #F1F5F9;
            font-size: 1.05rem;
            font-weight: 700;
            padding: 0 24px;
            border: none !important;
            transition: all 0.2s ease;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #06B6D4 0%, #2563EB 100%) !important;
            color: #FFFFFF !important;
            box-shadow: 0 4px 16px rgba(6, 182, 212, 0.5);
        }

        /* Button Customization */
        div.stButton > button {
            background: linear-gradient(135deg, #06B6D4 0%, #2563EB 100%);
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            font-size: 1.08rem !important;
            font-weight: 700 !important;
            border: none;
            border-radius: 12px;
            padding: 12px 28px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 16px rgba(6, 182, 212, 0.35);
        }

        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(6, 182, 212, 0.6);
            color: #FFFFFF !important;
        }

        /* DataFrame Table Container */
        [data-testid="stDataFrame"] {
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 14px !important;
            overflow: hidden !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
