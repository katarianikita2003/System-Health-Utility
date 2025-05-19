const express = require('express');
const cors = require('cors');
const app = express();
const port = 8000;

app.use(cors());

app.get('/report', (req, res) => {
  // Mock system health data - customize as needed
  const report = {
    timestamp: Date.now(),
    "DISK ENCRYPTION": {
      status: false,
      details: "BitLocker not fully encrypted or disabled"
    },
    "OS UPDATE": {
      status: false,
      details: "1 pending update(s)"
    },
    "ANTIVIRUS": {
      status: true,
      details: "Windows Defender 397568"
    },
    "INACTIVITY SLEEP": {
      status: true,
      details: "Sleep timeout set to 0 minutes"
    }
  };
  res.json(report);
});

app.listen(port, () => {
  console.log(`Mock system health server running at http://localhost:${port}`);
});
