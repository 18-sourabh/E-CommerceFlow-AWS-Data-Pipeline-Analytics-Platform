{{ config(materialized='table') }}

select
    order_id,
    max(payment_type) as primary_payment_type,
    max(payment_installments) as max_payment_installments,
    sum(payment_value) as total_payment_value
from {{ ref('stg_payments') }}
group by order_id