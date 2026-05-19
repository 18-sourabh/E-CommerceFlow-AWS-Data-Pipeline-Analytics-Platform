{{ config(materialized='table') }}

select

    -- Order grain
    oi.order_id,
    oi.order_item_id,

    -- Foreign keys
    o.customer_id,
    oi.product_id,
    oi.seller_id,
    date(o.order_purchase_timestamp) as order_date,

    -- Order info
    o.order_status,
    o.order_purchase_timestamp,

    -- Customer attributes
    c.customer_city,
    c.customer_state,

    -- Product attributes
    p.product_category_name,

    -- Seller attributes
    s.seller_city,
    s.seller_state,

    -- Measures
    oi.price,
    oi.freight_value,
    oi.price + oi.freight_value as total_item_value, 

    --Payments
    pay.primary_payment_type,
    pay.max_payment_installments,
    pay.total_payment_value,

    --Reviews
    r.review_score,
    r.first_review_date,

    --Aggregate
    date_diff('day', o.order_purchase_timestamp, o.order_delivered_customer_date) as delivery_days,

    date_diff('day', o.order_purchase_timestamp, o.order_estimated_delivery_date) as estimated_delivery_days,

    case
        when o.order_delivered_customer_date > o.order_estimated_delivery_date then 1
        else 0
    end as is_delayed

from {{ ref('stg_order_items') }} oi

left join {{ ref('stg_orders') }} o
    on oi.order_id = o.order_id

left join {{ ref('dim_customers') }} c
    on o.customer_id = c.customer_id

left join {{ ref('dim_products') }} p
    on oi.product_id = p.product_id

left join {{ ref('dim_sellers') }} s
    on oi.seller_id = s.seller_id

left join {{ ref('fct_order_payments') }} pay
    on oi.order_id = pay.order_id

left join {{ ref('fct_order_reviews') }} r
    on oi.order_id = r.order_id

