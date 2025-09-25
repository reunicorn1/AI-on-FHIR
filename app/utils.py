from datetime import datetime

from datetime import datetime
from collections import Counter

def calculate_age(birthdate: str) -> int | None:
    if not birthdate:
        return None
    try:
        birth_year = int(birthdate.split("-")[0])
        return datetime.now().year - birth_year
    except Exception:
        return None


def categorize_age(age: int) -> str:
    if age is None:
        return "unknown"
    if age <= 18:
        return "0-18"
    if age <= 35:
        return "19-35"
    if age <= 50:
        return "36-50"
    if age <= 65:
        return "51-65"
    return "66+"


def simplify_patient_data(fhir_response: dict, params: dict) -> dict:
    patients = []
    gender_counter = Counter()
    age_counter = Counter()
    city_counter = Counter()
    state_counter = Counter()

    for entry in fhir_response.get("entry", []):
        resource = entry.get("resource", {})
        if not resource:
            continue

        # --- Extract data ---
        name = ""
        if "name" in resource and resource["name"]:
            names = resource["name"][0]
            given = names.get("given", [""])
            family = names.get("family", "")
            name = f"{given[0]} {family}".strip()

        birthdate = resource.get("birthDate")
        age = calculate_age(birthdate)
        age_group = categorize_age(age)
        gender = resource.get("gender", "unknown")

        address = resource.get("address", [])
        city = address[0].get("city") if address else None
        state = address[0].get("state") if address else None

        patient = {
            "name": name,
            "gender": gender,
            "age": age,
            "age_group": age_group,
            "birthDate": birthdate,
            "city": city,
            "state": state,
        }

        if params.get("_has:Condition:patient:code"):
            patient["condition"] = params["_has:Condition:patient:code"]

        patients.append(patient)

        # --- Update counters in the same loop ---
        gender_counter[gender] += 1
        age_counter[age_group] += 1
        if city:
            city_counter[city] += 1
        if state:
            state_counter[state] += 1

    summary = {
        "total_patients": len(patients),
        "gender_distribution": dict(gender_counter),
        "age_distribution": dict(age_counter),
        "locations": {
            "cities": dict(city_counter),
            "states": dict(state_counter),
        }
    }

    return {
        "query": params,
        "summary": summary,
        "patients": patients,
    }
