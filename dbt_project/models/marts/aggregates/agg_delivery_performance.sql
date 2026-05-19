{{ config(materialized='table') }}

select
    customer_state,
    count(distinct order_id) as total_orders,
    avg(delivery_days) as avg_delivery_days,
    avg(estimated_delivery_days) as avg_estimated_delivery_days,
    sum(is_delayed) as delayed_items,
    cast(sum(is_delayed) as double) / count(*) as delay_rate,
    sum(total_item_value) as total_gmv
from {{ ref('fact_order_items') }}
where customer_state is not null
group by customer_state