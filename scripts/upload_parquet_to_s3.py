import boto3
from pathlib import Path

BUCKET_NAME = "sourabh-brazil-ecommerce-datalake"
LOCAL_PARQUET_PATH = Path("data/processed/parquet")

s3 = boto3.client("s3")


def upload_parquet_files():
    for file_path in LOCAL_PARQUET_PATH.rglob("*.parquet"):
        table_name = file_path.parent.name

        s3_key = f"staging/{table_name}/{file_path.name}"

        print(f"Uploading {file_path} to s3://{BUCKET_NAME}/{s3_key}")

        s3.upload_file(str(file_path), BUCKET_NAME, s3_key)

    print("Parquet upload completed.")


if __name__ == "__main__":
    upload_parquet_files()