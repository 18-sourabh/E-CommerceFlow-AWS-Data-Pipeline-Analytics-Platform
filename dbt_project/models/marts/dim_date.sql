{{ config(materialized='table') }}

with dates as (

    select distinct
        date(order_purchase_timestamp) as order_date
    from {{ ref('stg_orders') }}

)

select
    order_date as date_key,

    year(order_date) as year,
    month(order_date) as month,
    day(order_date) as day,

    quarter(order_date) as quarter,

    date_format(order_date, '%W') as weekday_name,
    date_format(order_date, '%M') as month_name

from dates