{{ config(materialized='view') }}

select
    order_id,
    order_item_id,
    product_id,
    seller_id,
    shipping_limit_date,
    cast(price as double) as price,
    cast(freight_value as double) as freight_value
from {{ source('brazil_ecommerce_staging', 'order_items') }}