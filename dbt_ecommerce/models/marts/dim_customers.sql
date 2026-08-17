WITH customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
)
SELECT
    customer_id,
    first_name || ' ' || last_name AS full_name,
    email,
    city,
    signup_date
FROM customers