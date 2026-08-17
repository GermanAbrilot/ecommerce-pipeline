WITH source AS (
    SELECT * FROM {{ source('raw_data', 'customers') }}
)
SELECT
    customer_id::INT AS customer_id,
    TRIM(first_name) AS first_name,
    TRIM(last_name) AS last_name,
    LOWER(TRIM(email)) AS email,
    TRIM(city) AS city,
    signup_date::DATE AS signup_date,
    _ingested_at
FROM source