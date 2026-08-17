WITH source AS (
    SELECT * FROM {{ source('raw_data', 'products') }}
)
SELECT
    TRIM(product_id) AS product_id,
    TRIM(product_name) AS product_name,
    TRIM(category) AS category,
    unit_price::NUMERIC(12,2) AS unit_price,
    _ingested_at
FROM source