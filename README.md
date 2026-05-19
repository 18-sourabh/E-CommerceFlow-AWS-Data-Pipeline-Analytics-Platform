# Brazil E-Commerce Data Pipeline

## Objective
Build a production-style ELT pipeline using AWS, dbt, Athena, Glue, S3, and Airflow.

## Architecture
Source CSVs → Python ingestion → S3 raw → Parquet staging → Glue Catalog → Athena → dbt models → Star schema → Aggregates → Airflow orchestration

## Tools Used
- Python
- AWS S3
- AWS Glue
- Amazon Athena
- dbt
- Apache Airflow
- Parquet
- SQL

## Key Features
- Hash-based change detection
- Metadata logging
- Raw/staging/curated data lake layers
- Parquet conversion
- Glue cataloging
- dbt staging models
- Star schema with fact and dimension tables
- dbt data quality tests
- Dashboard-ready aggregate tables
- Airflow orchestration with branching and retries

## Final Models
- fact_order_items
- dim_customers
- dim_products
- dim_sellers
- dim_date
- agg_monthly_sales
- agg_sales_by_state
- agg_sales_by_category
- agg_sales_by_payment_type
- agg_delivery_performance