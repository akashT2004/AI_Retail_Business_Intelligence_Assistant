import pandas as pd
from sqlalchemy import create_engine

# MySQL Connection
username = "root"
password = "AkashT#"
host = "localhost"
database = "ai_retail_bi"

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}/{database}"
)

# Read CSV
df = pd.read_csv("../data/product_master (1).csv")

# Rename columns to match MySQL table
df.columns = [
    "product_id",
    "product_name",
    "category",
    "sub_category"
]

# Import into MySQL
df.to_sql(
    "products",
    con=engine,
    if_exists="append",
    index=False
)

print("Products imported successfully!")
print("Rows Imported:", len(df))