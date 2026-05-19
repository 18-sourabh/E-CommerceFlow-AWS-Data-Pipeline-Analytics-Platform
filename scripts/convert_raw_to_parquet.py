import pandas as pd
from pathlib import Path

LOCAL_RAW_PATH = Path("data/raw")
LOCAL_PROCESSED_PATH = Path("data/processed/parquet")

DATASET_MAPPING = {
    "olist_customers_dataset.csv": "customers",
    "olist_geolocation_dataset.csv": "geolocation",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "payments",
    "olist_order_reviews_dataset.csv": "reviews",
    "olist_orders_dataset.csv": "orders",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "product_category_name_translation.csv": "product_category_translation",
}

LOCAL_PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

for file_path in LOCAL_RAW_PATH.glob("*.csv"):
    file_name = file_path.name

    if file_name not in DATASET_MAPPING:
        print(f"Skipping unknown file: {file_name}")
        continue

    table_name = DATASET_MAPPING[file_name]
    output_dir = LOCAL_PROCESSED_PATH / table_name
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Converting {file_name} to Parquet...")

    df = pd.read_csv(file_path)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    output_file = output_dir / f"{table_name}.parquet"
    df.to_parquet(output_file, index=False)

    print(f"Saved: {output_file}")

print("CSV to Parquet conversion completed.")