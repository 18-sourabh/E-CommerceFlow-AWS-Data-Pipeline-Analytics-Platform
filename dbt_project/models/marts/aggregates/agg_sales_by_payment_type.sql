{{ config(materialized='table') }}

select
    primary_payment_type,
    count(distinct order_id) as total_orders,
    count(*) as total_order_items,
    sum(total_item_value) as total_gmv,
    avg(total_item_value) as avg_item_value,
    avg(max_payment_installments) as avg_installments,
    avg(review_score) as avg_review_score
from {{ ref('fact_order_items') }}
where primary_payment_type is not null
group by primary_payment_type