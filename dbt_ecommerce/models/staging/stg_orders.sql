WITH source AS (
    SELECT * FROM {{ source('raw_data', 'orders') }}
)
SELECT
    order_id::INT AS order_id,
    customer_id::INT AS customer_id,
    order_date::TIMESTAMP AS order_date,
    UPPER(TRIM(order_status)) AS order_status,
    total_amount::NUMERIC(12,2) AS total_amount,
    _ingested_at
FROM source