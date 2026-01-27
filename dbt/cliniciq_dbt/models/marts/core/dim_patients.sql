SELECT
  patient_id,
  first_name,
  last_name,
  birth_date,
  sex,
  state,
  created_at,
  date_diff('year', birth_date, current_date) as age_years
FROM {{ ref('stg_patients') }}