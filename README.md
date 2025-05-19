# 🩺 System Health Monitor

A cross-platform system health monitoring tool that checks for OS updates, system sleep settings, and reports them via a Flask server with a simple web dashboard.

## 🚀 Features

* ✅ Check for OS updates on **Windows**, **macOS**, and **Linux**
* 💤 Detect system sleep/inactivity timeout settings
* 🌐 View reports via a **Flask-powered dashboard**
* 💾 Store all reports in a persistent JSON file
* 📤 Submit reports via a POST API endpoint

## 🗂️ Project Structure

```
project-root/
├── client/
│   ├── templates/
│   │   └── dashboard.html   # Frontend dashboard
├── server/
│   └── app.py               # Flask app
├── os_update.py             # OS update checker
├── sleep.py                 # Inactivity/sleep timeout checker
└── reports.json             # Stored system health reports
```

## 🛠️ Installation & Usage

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/system-health-monitor.git
cd system-health-monitor
```

### 2. Install Dependencies

Make sure you have Python 3.7+ and pip installed.

```bash
pip install Flask
```

### 3. Run the Flask Server

```bash
python server/app.py
```

> The dashboard will be available at: [http://localhost:8000/reports](http://localhost:8000/reports)

### 4. Submit a Health Report

You can write a script to collect and post the report to the Flask server like so:

```python
import requests
from os_update import check_os_update
from sleep import check_inactivity_sleep
from datetime import datetime

report = {
    "timestamp": datetime.utcnow().isoformat(),
    "os_update": check_os_update(),
    "sleep_timeout": check_inactivity_sleep()
}

requests.post("http://localhost:8000/report", json=report)
```

## 📋 API Endpoints

### `POST /report`

Submit a health report.

```json
{
  "timestamp": "...",
  "os_update": {"status": true, "details": "..."},
  "sleep_timeout": {"status": false, "details": "..."}
}
```

### `GET /reports`

Fetch all stored reports.

