SELECT
  encounter_id,
  patient_id,
  encounter_type,
  start_at,
  end_at,
  date_diff('minute', start_at, end_at) as duration_minutes,
  facility_id,
  provider_id
FROM {{ ref('stg_encounters') }}