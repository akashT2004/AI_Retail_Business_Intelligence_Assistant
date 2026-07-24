import os
import re
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai

from db_connection import get_engine, get_db_status

# Load environment variables
load_dotenv()

# Configure Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Load Gemini Model
try:
    model = genai.GenerativeModel("gemini-2.5-flash")
except Exception:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
    except Exception:
        model = None

# Database Schema
DATABASE_SCHEMA = """
Database Tables:

customers(
  customer_id,
  customer_name,
  segment,
  city,
  state,
  region
)

products(
  product_id,
  product_name,
  category,
  sub_category
)

orders(
  row_id,
  order_id,
  order_date,
  ship_date,
  ship_mode,
  customer_id,
  segment,
  city,
  state,
  region,
  product_id,
  category,
  sub_category,
  product_name,
  sales,
  quantity,
  profit,
  returns,
  payment_mode,
  warehouse,
  current_stock,
  reorder_level,
  lead_time_days
)
"""

def generate_sql(question):
    """Generates standard SQL query for SQLite / MySQL dialect."""
    if not model:
        raise ValueError("Google Gemini API is not configured or unavailable.")

    db_status = get_db_status()
    db_type = db_status.get("type", "sqlite").upper()

    prompt = f"""
You are an expert Senior SQL & Business Intelligence Developer.
Target SQL Dialect: {db_type} / ANSI SQL.

Database Schema:
{DATABASE_SCHEMA}

Rules:
1. Generate ONLY a valid SELECT query.
2. Never use DELETE, UPDATE, INSERT, DROP, ALTER, or TRUNCATE.
3. Use ROUND() for decimal aggregations (sales, profit).
4. Order results logically (e.g. ORDER BY Sales DESC or ORDER BY profit DESC).
5. If limiting, use LIMIT N clause.
6. Return ONLY the raw SQL statement.
7. No explanation text.
8. No markdown block enclosing code unless required (will be stripped).

Question:
{question}
"""

    response = model.generate_content(prompt)
    sql = response.text.strip()

    # Clean code fences
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"```", "", sql).strip()
    
    # Remove trailing semicolons if any
    sql = sql.rstrip(";")

    return sql

def run_query(sql):
    """Executes SQL query using SQLAlchemy engine."""
    engine = get_engine()
    df = pd.read_sql(sql, engine)
    return df

def generate_insight(question, df):
    """Generates AI business insight based on question and dataframe result."""
    if not model:
        return "Gemini AI model unavailable for insight generation."

    # Truncate dataframe for prompt if large
    sample_df = df.head(30)
    data_str = sample_df.to_string(index=False)

    prompt = f"""
You are an Executive Retail Business Intelligence Analyst.

User Question:
"{question}"

Query Result Data (Top rows):
{data_str}

Summary Stats:
Total Rows: {len(df)}

Task:
Provide a structured, executive-level business breakdown with:
1. 🎯 **Key Findings**: 2-3 bullet points summarizing what the data shows.
2. 💡 **Strategic Business Insights**: 2 high-level insights on revenue, profitability, product performance, or customer patterns.
3. 🚀 **Actionable Recommendations**: 2 concrete, actionable next steps for business leaders.

Keep tone professional, crisp, and direct. Use bold formatting and clean bullet points.
"""

    response = model.generate_content(prompt)
    return response.text