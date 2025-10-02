# seed_records.py
import json
import requests
from pathlib import Path

API = "http://127.0.0.1:8000/records"
DATA = Path("sample-registry.json")

def main():
    items = json.loads(DATA.read_text(encoding="utf-8"))
    for p in items:
        payload = {
            "project_name": p["project_name"],
            "registry": p["registry"],
            "vintage": p["vintage"],
            "quantity": p["quantity"],
            "serial_number": p.get("serial_number"),
        }
        r = requests.post(API, json=payload, timeout=10)
        try:
            print(p["project_name"], "->", r.status_code, r.json())
        except Exception:
            print(p["project_name"], "->", r.status_code, r.text)

if __name__ == "__main__":
    main()
