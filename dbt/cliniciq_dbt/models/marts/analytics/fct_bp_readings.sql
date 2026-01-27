WITH obs AS (
  SELECT * FROM {{ ref('stg_observations') }}
),

bp AS (
  SELECT
    encounter_id,
    patient_id,
    max(CASE WHEN code = '8480-6' THEN VALUE END) AS systolic,
    max(CASE WHEN code = '8462-4' THEN VALUE END) AS diastolic,
    min(observed_at) as first_observed_at
  FROM obs
  WHERE code in ('8480-6', '8462-4')
  GROUP BY 1,2
)

SELECT
  encounter_id,
  patient_id,
  systolic,
  diastolic,
  first_observed_at
FROM bp
WHERE systolic IS NOT NULL AND diastolic IS NOT NULL