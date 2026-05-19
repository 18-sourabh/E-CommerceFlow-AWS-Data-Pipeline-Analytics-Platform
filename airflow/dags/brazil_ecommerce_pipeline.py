from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator

PROJECT_ROOT = "/Users/sourabh18/Desktop/brazil-ecommerce-data-pipeline"
DBT_PROJECT = f"{PROJECT_ROOT}/dbt_project/brazil_ecommerce_dbt"
PYTHON_BIN = f"{PROJECT_ROOT}/venv/bin/python"
DBT_BIN = f"{PROJECT_ROOT}/venv/bin/dbt"

CHANGE_FLAG_FILE = Path(f"{PROJECT_ROOT}/data/processed/changes_detected.txt")

default_args = {
    "owner": "sourabh",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}


def decide_next_step():
    if not CHANGE_FLAG_FILE.exists():
        return "skip_pipeline"

    flag_value = CHANGE_FLAG_FILE.read_text().strip().lower()

    if flag_value == "true":
        return "convert_raw_to_parquet"

    return "skip_pipeline"


with DAG(
    dag_id="brazil_ecommerce_pipeline",
    default_args=default_args,
    description="End-to-end Brazil ecommerce data pipeline with conditional execution",
    start_date=datetime(2026, 5, 1),
    schedule=None,
    catchup=False,
    tags=["data-engineering", "aws", "dbt", "ecommerce"],
) as dag:

    start = EmptyOperator(
        task_id="start"
    )

    ingest_raw_to_s3 = BashOperator(
        task_id="ingest_raw_to_s3",
        bash_command=f"cd {PROJECT_ROOT} && {PYTHON_BIN} scripts/ingest_raw_to_s3.py",
    )

    check_changes = BranchPythonOperator(
        task_id="check_changes",
        python_callable=decide_next_step,
    )

    skip_pipeline = EmptyOperator(
        task_id="skip_pipeline"
    )

    convert_raw_to_parquet = BashOperator(
        task_id="convert_raw_to_parquet",
        bash_command=f"cd {PROJECT_ROOT} && {PYTHON_BIN} scripts/convert_raw_to_parquet.py",
    )

    upload_parquet_to_s3 = BashOperator(
        task_id="upload_parquet_to_s3",
        bash_command=f"cd {PROJECT_ROOT} && {PYTHON_BIN} scripts/upload_parquet_to_s3.py",
    )

    run_glue_crawler = BashOperator(
        task_id="run_glue_crawler",
        bash_command="aws glue start-crawler --name brazil_ecommerce_staging_crawler || true",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_PROJECT} && {DBT_BIN} run",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_PROJECT} && {DBT_BIN} test",
    )

    end = EmptyOperator(
        task_id="end",
        trigger_rule="none_failed_min_one_success",
    )

    start >> ingest_raw_to_s3 >> check_changes

    check_changes >> skip_pipeline >> end

    (
        check_changes
        >> convert_raw_to_parquet
        >> upload_parquet_to_s3
        >> run_glue_crawler
        >> dbt_run
        >> dbt_test
        >> end
    )