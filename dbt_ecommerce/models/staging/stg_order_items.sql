WITH source AS (
    SELECT * FROM {{ source('raw_data', 'order_items') }}
)
SELECT
    item_id::INT AS item_id,
    order_id::INT AS order_id,
    TRIM(product_id) AS product_id,
    quantity::INT AS quantity,
    unit_price::NUMERIC(12,2) AS unit_price,
    _ingested_at
FROM source