{{ config(materialized='view') }}

select
    order_id,
    payment_sequential,
    lower(payment_type) as payment_type,
    cast(payment_installments as integer) as payment_installments,
    cast(payment_value as double) as payment_value
from {{ source('brazil_ecommerce_staging', 'payments') }}