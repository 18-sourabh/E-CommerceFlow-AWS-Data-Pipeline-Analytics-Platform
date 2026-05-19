from flask import Flask, render_template
from pyathena import connect
import pandas as pd
import plotly.express as px
import plotly.io as pio
import json
from pathlib import Path

app = Flask(__name__)

ATHENA_DATABASE = "brazil_ecommerce_curated"
ATHENA_STAGING_DIR = "s3://sourabh-athena-query-results/"
AWS_REGION = "us-east-1"

BASE_DIR = Path(__file__).resolve().parent
BRAZIL_GEOJSON_PATH = BASE_DIR / "static" / "data" / "brazil_states.geojson"


def run_query(query: str) -> pd.DataFrame:
    conn = connect(
        s3_staging_dir=ATHENA_STAGING_DIR,
        region_name=AWS_REGION,
        schema_name=ATHENA_DATABASE,
    )
    return pd.read_sql(query, conn)


@app.route("/")
def dashboard():
    monthly_sales = run_query("""
        select *
        from agg_monthly_sales
        order by order_year, order_month
    """)

    sales_by_state = run_query("""
        select *
        from agg_sales_by_state
        order by total_gmv desc
    """)

    sales_by_category = run_query("""
        select *
        from agg_sales_by_category
        order by total_gmv desc
    """)

    sales_by_payment = run_query("""
        select *
        from agg_sales_by_payment_type
        order by total_gmv desc
    """)

    delivery = run_query("""
        select *
        from agg_delivery_performance
        order by delay_rate desc
    """)

    kpis = run_query("""
        select
            sum(total_item_value) as total_sales,
            count(distinct order_id) as total_orders,
            count(*) as total_items_sold,
            avg(total_item_value) as avg_order_item_value,
            avg(review_score) as avg_review_score,
            avg(delivery_days) as avg_delivery_days
        from fact_order_items
    """).iloc[0]

    monthly_sales["period"] = (
        monthly_sales["order_year"].astype(str)
        + "-"
        + monthly_sales["order_month"].astype(str).str.zfill(2)
    )

    sales_trend_fig = px.line(
        monthly_sales,
        x="period",
        y="total_gmv",
        markers=True,
        title="Sales Over Time",
    )

    state_fig = px.bar(
        sales_by_state.head(10),
        x="customer_state",
        y="total_gmv",
        title="Top States by Sales",
    )

    category_fig = px.pie(
        sales_by_category.head(10),
        names="product_category_name",
        values="total_gmv",
        hole=0.55,
        title="Sales by Category",
    )

    payment_fig = px.bar(
        sales_by_payment,
        x="total_gmv",
        y="primary_payment_type",
        orientation="h",
        title="Sales by Payment Type",
    )

    delivery_fig = px.bar(
        delivery.head(10),
        x="customer_state",
        y="avg_delivery_days",
        title="Average Delivery Days by State",
    )

    product_fig = px.bar(
        sales_by_category.head(10),
        x="total_gmv",
        y="product_category_name",
        orientation="h",
        title="Top Product Categories by Sales",
    )

    # Customer Brazil heat map
    if BRAZIL_GEOJSON_PATH.exists():
        with open(BRAZIL_GEOJSON_PATH, "r") as f:
            brazil_geojson = json.load(f)

        customer_fig = px.choropleth(
            sales_by_state,
            geojson=brazil_geojson,
            locations="customer_state",
            featureidkey="properties.sigla",
            color="total_orders",
            color_continuous_scale="Blues",
            title="Customer Orders by Brazilian State",
        )

        customer_fig.update_geos(
            fitbounds="locations",
            visible=False
        )
    else:
        customer_fig = px.bar(
            sales_by_state.head(10),
            x="customer_state",
            y="total_orders",
            title="Top Customer States by Orders",
        )

    charts = {
        "sales_trend": pio.to_html(sales_trend_fig, full_html=False),
        "state": pio.to_html(state_fig, full_html=False),
        "category": pio.to_html(category_fig, full_html=False),
        "payment": pio.to_html(payment_fig, full_html=False),
        "delivery": pio.to_html(delivery_fig, full_html=False),
        "customer": pio.to_html(customer_fig, full_html=False),
        "product": pio.to_html(product_fig, full_html=False),
    }

    return render_template(
        "index.html",
        kpis=kpis,
        charts=charts,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)