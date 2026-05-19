{{ config(materialized='table') }}

select
    product_category_name,
    count(distinct order_id) as total_orders,
    count(*) as total_order_items,
    sum(price) as product_revenue,
    sum(freight_value) as freight_revenue,
    sum(total_item_value) as total_gmv,
    avg(total_item_value) as avg_item_value,
    avg(review_score) as avg_review_score,
    avg(delivery_days) as avg_delivery_days,
    sum(is_delayed) as delayed_items
from {{ ref('fact_order_items') }}
where product_category_name is not null
group by product_category_name