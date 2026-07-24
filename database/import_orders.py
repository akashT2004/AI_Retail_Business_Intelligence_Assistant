import pandas as pd
from sqlalchemy import create_engine

# -----------------------------
# MySQL Connection
# -----------------------------
username = "root"
password = "AkashT#"
host = "localhost"
database = "ai_retail_bi"

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}/{database}"
)

# -----------------------------
# Read CSV
# -----------------------------
df = pd.read_csv("../data/SuperStore_Sales_Enhanced.csv")

# -----------------------------
# Rename Columns
# -----------------------------
df.columns = [
    "row_id",
    "order_id",
    "order_date",
    "ship_date",
    "ship_mode",
    "customer_id",
    "customer_name",
    "segment",
    "country",
    "city",
    "state",
    "region",
    "product_id",
    "category",
    "sub_category",
    "product_name",
    "sales",
    "quantity",
    "profit",
    "returns",
    "payment_mode",
    "ind1",
    "ind2",
    "warehouse",
    "current_stock",
    "reorder_level",
    "lead_time_days"
]

# -----------------------------
# Keep only MySQL columns
# -----------------------------
orders = df[
    [
        "order_id",
        "order_date",
        "ship_date",
        "ship_mode",
        "customer_id",
        "segment",
        "city",
        "state",
        "region",
        "product_id",
        "category",
        "sub_category",
        "product_name",
        "sales",
        "quantity",
        "profit",
        "returns",
        "payment_mode",
        "warehouse",
        "current_stock",
        "reorder_level",
        "lead_time_days"
    ]
]

# -----------------------------
# Convert Dates
# -----------------------------
orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    dayfirst=True
)

orders["ship_date"] = pd.to_datetime(
    orders["ship_date"],
    dayfirst=True
)

# -----------------------------
# Import
# -----------------------------
orders.to_sql(
    "orders",
    engine,
    if_exists="append",
    index=False
)

print("=" * 50)
print("Orders imported successfully!")
print("Rows Imported:", len(orders))
print("=" * 50)