with src as (
    SELECT * FROM {{ ref('encounters') }}
)

SELECT
    encounter_id,
    patient_id,
    encounter_type,
    cast(start_at as timestamp) as start_at,
    cast(end_at as timestamp) as end_at,
    facility_id,
    provider_id
FROM src