import csv
import random
import uuid
from datetime import datetime, timedelta, date
from pathlib import Path

random.seed(42)

BASE_DIR = Path(__file__).resolve().parents[1]
OUT_DIR = BASE_DIR / "sample_Data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

N_PATIENTS = 250
MIN_ENCOUNTERS_PER_PATIENT = 1
MAX_ENCOUNTERS_PER_PATIENT = 6

# A small set of realistic-ish observation types (mix of vitals + common labs)
OBS_DEFS = [
    {"code_system": "LOINC", "code": "8480-6", "name": "Systolic blood pressure", "unit": "mmHg", "min": 90, "max": 170},
    {"code_system": "LOINC", "code": "8462-4", "name": "Diastolic blood pressure", "unit": "mmHg", "min": 55, "max": 105},
    {"code_system": "LOINC", "code": "8867-4", "name": "Heart rate", "unit": "bpm", "min": 50, "max": 140},
    {"code_system": "LOINC", "code": "8310-5", "name": "Body temperature", "unit": "C", "min": 35.8, "max": 39.5},
    {"code_system": "LOINC", "code": "2345-7", "name": "Glucose", "unit": "mg/dL", "min": 70, "max": 260},
    {"code_system": "LOINC", "code": "4548-4", "name": "Hemoglobin A1c", "unit": "%", "min": 4.8, "max": 12.5},
]

ENCOUNTER_TYPES = ["outpatient", "inpatient", "urgent_care", "telehealth"]
SEXES = ["F", "M"]
STATES = ["CA", "TX", "FL", "NY", "IL", "AZ", "WA", "CO", "MA", "GA"]


def rand_date(start: date, end: date) -> date:
    delta_days = (end - start).days
    return start + timedelta(days=random.randint(0, delta_days))


def rand_datetime(start: datetime, end: datetime) -> datetime:
    delta_seconds = int((end - start).total_seconds())
    return start + timedelta(seconds=random.randint(0, delta_seconds))


def make_patient_id(i: int) -> str:
    return f"PAT-{i:05d}"


def write_patients(path: Path) -> list[dict]:
    today = date.today()
    patients = []

    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "patient_id",
                "first_name",
                "last_name",
                "birth_date",
                "sex",
                "state",
                "created_at",
            ],
        )
        w.writeheader()

        for i in range(1, N_PATIENTS + 1):
            pid = make_patient_id(i)
            birth = rand_date(today - timedelta(days=365 * 85), today - timedelta(days=365 * 18))
            created = datetime.combine(rand_date(today - timedelta(days=365 * 3), today), datetime.min.time())

            row = {
                "patient_id": pid,
                "first_name": f"First{i}",
                "last_name": f"Last{i}",
                "birth_date": birth.isoformat(),
                "sex": random.choice(SEXES),
                "state": random.choice(STATES),
                "created_at": created.isoformat(),
            }
            patients.append(row)
            w.writerow(row)

    return patients


def write_encounters(path: Path, patients: list[dict]) -> list[dict]:
    encounters = []
    now = datetime.now()
    start_window = now - timedelta(days=365 * 2)

    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "encounter_id",
                "patient_id",
                "encounter_type",
                "start_at",
                "end_at",
                "facility_id",
                "provider_id",
            ],
        )
        w.writeheader()

        for p in patients:
            n_enc = random.randint(MIN_ENCOUNTERS_PER_PATIENT, MAX_ENCOUNTERS_PER_PATIENT)
            for _ in range(n_enc):
                start_at = rand_datetime(start_window, now - timedelta(days=1))
                duration_minutes = random.choice([15, 20, 30, 45, 60, 90, 120, 240, 480])
                end_at = start_at + timedelta(minutes=duration_minutes)

                enc_id = f"ENC-{uuid.uuid4().hex[:12].upper()}"
                row = {
                    "encounter_id": enc_id,
                    "patient_id": p["patient_id"],
                    "encounter_type": random.choice(ENCOUNTER_TYPES),
                    "start_at": start_at.isoformat(),
                    "end_at": end_at.isoformat(),
                    "facility_id": f"FAC-{random.randint(1, 25):03d}",
                    "provider_id": f"PRV-{random.randint(1, 120):04d}",
                }
                encounters.append(row)
                w.writerow(row)

    return encounters


def write_observations(path: Path, encounters: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "observation_id",
                "encounter_id",
                "patient_id",
                "code_system",
                "code",
                "name",
                "value",
                "unit",
                "observed_at",
            ],
        )
        w.writeheader()

        for enc in encounters:
            # 3–8 observations per encounter
            n_obs = random.randint(3, 8)
            obs_at_base = datetime.fromisoformat(enc["start_at"]) + timedelta(minutes=random.randint(0, 10))
            chosen = random.sample(OBS_DEFS, k=min(n_obs, len(OBS_DEFS)))

            for od in chosen:
                obs_id = f"OBS-{uuid.uuid4().hex[:12].upper()}"

                # numeric value (float for temp/A1c; int for most others)
                if isinstance(od["min"], float) or isinstance(od["max"], float) or od["unit"] in ["C", "%"]:
                    val = round(random.uniform(float(od["min"]), float(od["max"])), 1)
                else:
                    val = random.randint(int(od["min"]), int(od["max"]))

                observed_at = obs_at_base + timedelta(minutes=random.randint(0, 30))

                w.writerow(
                    {
                        "observation_id": obs_id,
                        "encounter_id": enc["encounter_id"],
                        "patient_id": enc["patient_id"],
                        "code_system": od["code_system"],
                        "code": od["code"],
                        "name": od["name"],
                        "value": val,
                        "unit": od["unit"],
                        "observed_at": observed_at.isoformat(),
                    }
                )


def main():
    patients_path = OUT_DIR / "patients.csv"
    encounters_path = OUT_DIR / "encounters.csv"
    observations_path = OUT_DIR / "observations.csv"

    patients = write_patients(patients_path)
    encounters = write_encounters(encounters_path, patients)
    write_observations(observations_path, encounters)

    print("Wrote:")
    print(f"- {patients_path} ({len(patients)} rows)")
    print(f"- {encounters_path} ({len(encounters)} rows)")
    # observations are variable; approximate count:
    print(f"- {observations_path} (~{len(encounters) * 5} rows est)")


if __name__ == "__main__":
    main()