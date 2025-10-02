import threading
import requests

API = "http://127.0.0.1:8000/records/9f57bf954e9ff2a9/retire"

def retire_credit():
    r = requests.post(API)
    print(f"Status: {r.status_code}, Response: {r.json()}")

threads = [threading.Thread(target=retire_credit) for _ in range(2)]

for t in threads:
    t.start()
for t in threads:
    t.join()
