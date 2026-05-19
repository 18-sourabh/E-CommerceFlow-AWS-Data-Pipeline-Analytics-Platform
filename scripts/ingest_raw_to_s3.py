import boto3
import csv
import hashlib
from pathlib import Path
from datetime import datetime, timezone

BUCKET_NAME = "sourabh-brazil-ecommerce-datalake"

LOCAL_RAW_PATH = Path("data/raw")
PROCESSED_PATH = Path("data/processed")
LOG_FILE = PROCESSED_PATH / "ingestion_log.csv"
CHANGE_FLAG_FILE = PROCESSED_PATH / "changes_detected.txt"

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

s3 = boto3.client("s3")


def calculate_file_hash(file_path):
    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(block)

    return sha256_hash.hexdigest()


def read_ingestion_log():
    if not LOG_FILE.exists():
        return {}

    latest_hash_by_file = {}

    with open(LOG_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if row.get("status") == "SUCCESS":
                latest_hash_by_file[row["file_name"]] = row.get("file_hash")

    return latest_hash_by_file


def write_log(file_name, file_hash, s3_key, status):
    file_exists = LOG_FILE.exists()

    with open(LOG_FILE, "a", newline="") as f:
        fieldnames = [
            "file_name",
            "file_hash",
            "s3_key",
            "status",
            "ingested_at",
        ]

        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "file_name": file_name,
            "file_hash": file_hash,
            "s3_key": s3_key,
            "status": status,
            "ingested_at": datetime.now(timezone.utc).isoformat(),
        })


def ingest_files():
    PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

    latest_hash_by_file = read_ingestion_log()
    ingestion_date = datetime.now().strftime("%Y-%m-%d")
    changes_detected = False

    for file_path in LOCAL_RAW_PATH.glob("*.csv"):
        file_name = file_path.name

        if file_name not in DATASET_MAPPING:
            print(f"Skipping unknown file: {file_name}")
            continue

        current_hash = calculate_file_hash(file_path)
        previous_hash = latest_hash_by_file.get(file_name)

        if previous_hash == current_hash:
            print(f"No change detected, skipping: {file_name}")
            continue

        dataset_name = DATASET_MAPPING[file_name]

        s3_key = (
            f"raw/{dataset_name}/"
            f"ingestion_date={ingestion_date}/"
            f"{file_name}"
        )

        print(f"Change detected. Uploading {file_name}")
        print(f"s3://{BUCKET_NAME}/{s3_key}")

        try:
            s3.upload_file(str(file_path), BUCKET_NAME, s3_key)
            write_log(file_name, current_hash, s3_key, "SUCCESS")
            changes_detected = True
            print(f"Uploaded successfully: {file_name}")

        except Exception as e:
            write_log(file_name, current_hash, s3_key, f"FAILED: {str(e)}")
            print(f"Upload failed for {file_name}: {e}")
            raise

    CHANGE_FLAG_FILE.write_text("true" if changes_detected else "false")

    print(f"Changes detected: {changes_detected}")
    print("Ingestion completed.")


if __name__ == "__main__":
    ingest_files()