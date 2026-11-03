import csv
import json
from pathlib import Path

EXPORT_DIR = Path(__file__).resolve().parent / "exports"
EXPORT_DIR.mkdir(exist_ok=True)
FIELDS = ["id", "city", "temperature", "humidity", "wind_speed", "pressure", "weather_condition", "recorded_at"]

def export_csv(records, path=None):
    target = Path(path) if path else EXPORT_DIR / "weather_records.csv"
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)
    return target

def export_json(records, path=None):
    target = Path(path) if path else EXPORT_DIR / "weather_records.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as handle:
        json.dump(records, handle, indent=2, ensure_ascii=False)
    return target

def import_csv(path):
    with Path(path).open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def import_json(path):
    with Path(path).open("r", encoding="utf-8") as handle:
        result = json.load(handle)
    if not isinstance(result, list):
        raise ValueError("JSON file must contain a list of records.")
    return result
