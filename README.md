# ClinicIQ

ClinicIQ is a healthcare analytics infrastructure project that demonstrates how EMR-style data can be ingested, validated, and transformed into analytics-ready datasets.

The project prioritizes **structure, correctness, and repeatability** over UI or visualization. It is intentionally designed as an internal analytics platform rather than a demo application.

---

## System Overview

ClinicIQ is composed of three clearly separated layers:

1. **Application layer** — FastAPI
2. **Analytics engineering layer** — dbt
3. **Data generation layer** — synthetic EMR-style data

This separation mirrors real-world healthcare analytics systems and allows each concern to evolve independently.

---

## Repository Structure
ClinicIQ/
├── src/                     # Application layer
│   ├── main.py               # FastAPI entry point
│   ├── db.py                 # DuckDB access helpers
│   └── insights.py           # Analytics-backed endpoints
│
├── scripts/                 # Data generation utilities
│   └── generate_synthetic_emr_csvs.py
│
├── sample_data/              # Canonical example EMR-style data
│   ├── patients.csv
│   ├── encounters.csv
│   └── observations.csv
│
├── dbt/
│   └── cliniciq_dbt/         # Analytics engineering layer
│       ├── models/
│       │   ├── staging/
│       │   └── marts/
│       │       ├── core/
│       │       └── analytics/
│       ├── schema.yml        # Model documentation + data tests
│       └── dbt_project.yml
│
└── README.md

Runtime artifacts (DuckDB files, dbt targets, logs) are excluded from version control.

---

## Analytics Engineering (dbt)

ClinicIQ includes a production-style dbt project that models EMR-style healthcare data into analytics-ready marts using DuckDB for local development.

### Data Inputs
Synthetic EMR-style CSVs:
- `patients`
- `encounters`
- `observations`

These datasets are generated locally and are safe to commit.

---

### dbt Models

#### Staging Layer
Typed, normalized representations of source data:
- `stg_patients`
- `stg_encounters`
- `stg_observations`

#### Core Marts
Conformed entities used across analytics:
- `dim_patients` — patient dimension with derived age
- `fct_encounters` — encounter-level fact table

#### Analytics Marts
Derived metrics intended for downstream consumption:
- `fct_bp_readings` — systolic and diastolic blood pressure per encounter

---

### Data Quality

Data quality is enforced using dbt tests:
- `not_null`
- `unique`

Tests are applied across staging models and marts to ensure analytical correctness.

---

## Application Layer

The FastAPI application is structured to consume analytics-ready outputs rather than raw data.

- `main.py` defines the application and routes
- `db.py` abstracts database access (DuckDB locally)
- `insights.py` exposes analytics-backed endpoints

This mirrors how analytics marts are typically served to downstream services in production environments.

---

## Running Locally

### 1. Environment setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Generate synthetic EMR-style data
```bash
python scripts/generate_synthetic_emr_csvs.py
```

### 3. Build analytics models
```bash
cd dbt/cliniciq_dbt
dbt seed --full-refresh
dbt build
```

### 4. Run the API
```bash
python src/main.py
```

### (Optional)

```bash
dbt docs generate
dbt docs serve
```
### Design Principles
	•	Clear separation between ingestion, transformation, and consumption
	•	Analytics models treated as first-class assets
	•	Explicit transformations and tests over implicit assumptions
	•	Infrastructure designed to remain understandable as complexity grows

### Purpose
ClinicIQ reflects how healthcare analytics systems should be built before scale:
with clarity, validation, and intentional structure, so they remain reliable as complexity increases.
