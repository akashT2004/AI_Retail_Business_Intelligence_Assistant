import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "AkashT#")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "ai_retail_bi")

_engine = None
_db_status = {"type": "unknown", "message": ""}

def _init_sqlite_engine():
    """Fallback engine using SQLite loaded from CSV files."""
    global _db_status
    engine = create_engine("sqlite:///:memory:", echo=False)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(base_dir, "..", "data"))
    
    # 1. Load Orders
    orders_csv = os.path.join(data_dir, "SuperStore_Sales_Enhanced.csv")
    if os.path.exists(orders_csv):
        df_orders = pd.read_csv(orders_csv)
        # Rename columns to standard schema
        df_orders.columns = [
            "row_id", "order_id", "order_date", "ship_date", "ship_mode",
            "customer_id", "customer_name", "segment", "country", "city",
            "state", "region", "product_id", "category", "sub_category",
            "product_name", "sales", "quantity", "profit", "returns",
            "payment_mode", "ind1", "ind2", "warehouse", "current_stock",
            "reorder_level", "lead_time_days"
        ]
        orders = df_orders[[
            "order_id", "order_date", "ship_date", "ship_mode", "customer_id",
            "segment", "city", "state", "region", "product_id", "category",
            "sub_category", "product_name", "sales", "quantity", "profit",
            "returns", "payment_mode", "warehouse", "current_stock",
            "reorder_level", "lead_time_days"
        ]].copy()
        
        orders["order_date"] = pd.to_datetime(orders["order_date"], dayfirst=True, errors="coerce").dt.strftime("%Y-%m-%d")
        orders["ship_date"] = pd.to_datetime(orders["ship_date"], dayfirst=True, errors="coerce").dt.strftime("%Y-%m-%d")
        orders.to_sql("orders", engine, if_exists="replace", index=False)

    # 2. Load Customers
    cust_csv = os.path.join(data_dir, "customer_master.csv")
    if os.path.exists(cust_csv):
        df_cust = pd.read_csv(cust_csv)
        df_cust.columns = ["customer_id", "customer_name", "segment", "city", "state", "region"]
        df_cust.to_sql("customers", engine, if_exists="replace", index=False)

    # 3. Load Products
    prod_csv = os.path.join(data_dir, "product_master (1).csv")
    if os.path.exists(prod_csv):
        df_prod = pd.read_csv(prod_csv)
        df_prod.columns = ["product_id", "product_name", "category", "sub_category"]
        df_prod.to_sql("products", engine, if_exists="replace", index=False)

    _db_status = {
        "type": "sqlite",
        "message": "SQLite (CSV Data Engine Active)"
    }
    return engine

def get_engine():
    global _engine, _db_status
    if _engine is not None:
        return _engine

    # Try MySQL first
    mysql_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    try:
        engine = create_engine(mysql_url, connect_args={"connect_timeout": 3})
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        _engine = engine
        _db_status = {
            "type": "mysql",
            "message": "MySQL Database Connected"
        }
        return _engine
    except Exception:
        # Fallback to SQLite
        _engine = _init_sqlite_engine()
        return _engine

def get_db_status():
    get_engine()
    return _db_status

if __name__ == "__main__":
    eng = get_engine()
    print("Status:", get_db_status())
    with eng.connect() as conn:
        res = conn.execute(text("SELECT COUNT(*) FROM orders")).fetchone()
        print("Orders count:", res[0])