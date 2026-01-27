with src as (
    SELECT * FROM {{ ref('observations') }}
)

SELECT
    observation_id,
    encounter_id,
    patient_id,
    code_system,
    code,
    name,
    cast(value as double) as value,
    unit,
    cast(observed_at as timestamp) as observed_at
FROM src