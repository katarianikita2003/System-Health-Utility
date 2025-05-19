import time
import json
import requests
import os
from .main import run_all_checks

CHECK_INTERVAL = 900  # 15 minutes (900 seconds)
LAST_STATE_FILE = "client/last_check.json"
API_ENDPOINT = "http://localhost:8000/report"

def load_last_state():
    if os.path.exists(LAST_STATE_FILE):
        with open(LAST_STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_current_state(state):
    with open(LAST_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def has_changed(new_state, last_state):
    return new_state != last_state


def send_to_api(data):
    try:
        response = requests.post(API_ENDPOINT, json=data)
        if response.status_code == 200:
            print("✅ Data sent successfully.")
        else:
            print(f"⚠️ Failed to send data: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error sending data: {e}")

def daemon_loop():
    while True:
        current_state = run_all_checks()
        last_state = load_last_state()

        if has_changed(current_state, last_state):
            send_to_api(current_state)
            save_current_state(current_state)
        else:
            print("No change detected, skipping API call.")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    daemon_loop()
