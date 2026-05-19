{{ config(materialized='table') }}

select
    order_id,
    max(review_score) as review_score,
    min(review_creation_date) as first_review_date,
    max(review_answer_timestamp) as latest_review_answer_timestamp
from {{ ref('stg_reviews') }}
group by order_id