WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),
order_items AS (
    SELECT * FROM {{ ref('stg_order_items') }}
)
SELECT
    o.order_id,
    o.customer_id,
    o.order_date,
    o.order_status,
    COUNT(i.item_id) AS total_items,
    SUM(i.quantity * i.unit_price) AS calculated_total_amount
FROM orders o
LEFT JOIN order_items i ON o.order_id = i.order_id
GROUP BY o.order_id, o.customer_id, o.order_date, o.order_status