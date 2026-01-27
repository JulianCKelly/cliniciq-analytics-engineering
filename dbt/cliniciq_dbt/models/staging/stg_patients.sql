with src as (
    SELECT * FROM {{ ref('patients') }}
)

SELECT
    patient_id,
    first_name,
    last_name,
    cast(birth_date as date) as birth_date,
    sex,
    state,
    cast(created_at as timestamp) as created_at
FROM src