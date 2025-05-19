from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from copy import deepcopy
import os

app = FastAPI()
from datetime import datetime

# Static files for dashboard UI
app.mount("/dashboard", StaticFiles(directory="client/templates", html=True), name="dashboard")

# In-memory store for latest report
latest_report = {
    "disk_encryption": {
        "status": False,
        "details": "BitLocker not fully encrypted or disabled"
    },
    "os_update": {
        "status": False,
        "details": "1 pending update(s)"
    },
    "antivirus": {
        "status": True,
        "details": "Windows Defender 397568"
    },
    "inactivity_sleep": {
        "status": True,
        "details": "Sleep timeout set to 0 minutes"
    }
}

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/report")
async def receive_report(request: Request):
    global latest_report
    latest_report = await request.json()
    print("📦 Received Report:", latest_report)  # 👈 Add this
    return {"message": "Report received successfully"}

@app.get("/report")
async def get_report():
    report_copy = deepcopy(latest_report)
    report_copy['timestamp'] = datetime.utcnow().isoformat() + "Z"
    return report_copy

@app.get("/")  # Optional: to open dashboard at root
def get_dashboard():
    return FileResponse("client/templates/dashboard.html")
