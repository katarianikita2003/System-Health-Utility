from flask import Flask, request, jsonify
from datetime import datetime
import os
import json

app = Flask(__name__)
DATA_FILE = "reports.json"

# Load previous reports
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        reports = json.load(f)
else:
    reports = []

@app.route("/report", methods=["POST"])
def receive_report():
    data = request.get_json()
    data["received_at"] = datetime.utcnow().isoformat()
    reports.append(data)

    # Save to file
    with open(DATA_FILE, "w") as f:
        json.dump(reports, f, indent=2)

    return jsonify({"status": "success", "message": "Report received"}), 200

@app.route("/reports", methods=["GET"])
def get_reports():
    return jsonify(reports)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
