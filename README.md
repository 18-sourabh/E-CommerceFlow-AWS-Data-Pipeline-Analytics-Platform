# CommerceFlow AI — End-to-End E-Commerce Data Engineering Platform

## Overview

CommerceFlow AI is a production-style end-to-end data engineering and analytics platform built using AWS, dbt, Apache Airflow, and Flask.

The project ingests raw e-commerce data, processes it through a scalable ELT architecture, builds analytical models using star-schema design, orchestrates workflows with Airflow, and delivers business insights through an interactive dashboard.

---

## Architecture

Raw CSV Data
↓
Python Ingestion Layer
↓
Amazon S3 (Raw Layer)
↓
Parquet Conversion
↓
Amazon S3 (Processed Layer)
↓
AWS Glue Data Catalog
↓
Amazon Athena
↓
dbt Transformations
↓
Star Schema Models
↓
Aggregate Business Tables
↓
Apache Airflow Orchestration
↓
Flask Analytics Dashboard

---

## Tech Stack

### Cloud
- Amazon S3
- AWS Glue
- Amazon Athena

### Data Engineering
- Python
- SQL
- dbt
- Apache Airflow
- Parquet

### Analytics & Dashboard
- Flask
- Plotly
- HTML/CSS

### Development
- Git
- GitHub

---

## Key Features

### Data Ingestion
- Hash-based file change detection
- Metadata-driven ingestion logging
- Incremental processing behavior
- Raw data storage in S3

### Data Transformation
- dbt staging models
- Fact and dimension table creation
- Star-schema implementation
- Aggregate reporting models

### Workflow Orchestration
- Airflow DAG orchestration
- Retry handling
- Conditional task execution
- Skip processing when no new data exists

### Analytics
- Interactive Flask dashboard
- KPI monitoring
- Customer insights
- Delivery performance
- Product analytics
- Payment analysis

---

## Data Models

### Fact Tables

- fact_order_items

### Dimension Tables

- dim_customers
- dim_products
- dim_sellers

### Aggregate Tables

- agg_monthly_sales
- agg_sales_by_state
- agg_sales_by_category
- agg_sales_by_payment_type
- agg_delivery_performance

---

## Dashboard Features

### Executive Overview
- Total Sales
- Total Orders
- Total Items Sold
- Average Order Value
- Average Review Score
- Average Delivery Days

### Sales Analytics
- Monthly sales trends
- State-level sales performance
- Product category analysis

### Customer Analytics
- Customer geographic heat map

### Delivery Analytics
- Delivery performance metrics

### Payment Analytics
- Payment method insights

---

## Airflow Pipeline

Current orchestration flow:

```text
ingest_raw_to_s3
        ↓
check_changes
   ↓          ↓
skip      convert_raw_to_parquet
                  ↓
         upload_parquet_to_s3
                  ↓
          run_glue_crawler
                  ↓
               dbt_run
                  ↓
              dbt_test
                  ↓
                 end
```

---

## Project Screenshots

### Architecture Diagram

Add:

```text
docs/architecture_diagram.png
```

### Airflow DAG

Add:

```text
docs/screenshots/airflow_dag_success_run.png
```


## Future Improvements

- Docker containerization
- MWAA deployment
- CI/CD with GitHub Actions
- Real-time streaming with Kafka
- ML-based recommendation engine
- User authentication

---

## Author

Sourabh Shinde

GitHub:
https://github.com/18-sourabh