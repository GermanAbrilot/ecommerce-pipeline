WITH products AS (
    SELECT * FROM {{ ref('stg_products') }}
)
SELECT
    product_id,
    product_name,
    category,
    unit_price
FROM products