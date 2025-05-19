from checks.antivirus import check_antivirus
from checks.disk_encryption import check_disk_encryption
from checks.os_update import check_os_update
from checks.sleep import check_inactivity_sleep
import platform
import json
import time

def run_all_checks():
    results = {
        "platform": platform.system(),
        "antivirus": check_antivirus(),
        "disk_encryption": check_disk_encryption(),
        "os_update": check_os_update(),
        "inactivity_sleep": check_inactivity_sleep(),
        "timestamp": time.time()
    }
    return results

if __name__ == "__main__":
    results = run_all_checks()
    print(json.dumps(results, indent=2))


