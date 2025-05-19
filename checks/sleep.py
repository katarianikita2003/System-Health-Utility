import platform
import subprocess
import re

def check_inactivity_sleep():
    system = platform.system()
    if system == "Windows":
        return check_windows_sleep()
    elif system == "Darwin":
        return check_macos_sleep()
    elif system == "Linux":
        return check_linux_sleep()
    else:
        return {"status": False, "details": f"Unsupported OS: {system}"}

def check_windows_sleep():
    try:
        scheme_output = subprocess.check_output(['powercfg', '/getactivescheme'], text=True)
        match = re.search(r'GUID: ([\w-]+)', scheme_output)
        if not match:
            return {"status": False, "details": "Could not find active power scheme"}

        scheme_guid = match.group(1)

        settings_output = subprocess.check_output(['powercfg', '/q', scheme_guid], text=True)

        sleep_timeout_pattern = re.compile(
            r'Power Setting GUID: 29f6c1db-86da-48c5-9fdb-f2b67b1f44da.*?Current AC Power Setting Index: (\d+)',
            re.DOTALL | re.IGNORECASE
        )
        sleep_match = sleep_timeout_pattern.search(settings_output)

        if sleep_match:
            seconds = int(sleep_match.group(1))
            minutes = seconds // 60
            status = minutes <= 10
            return {"status": status, "details": f"Sleep timeout set to {minutes} minutes"}
        else:
            return {"status": False, "details": "Sleep timeout setting not found in power scheme"}
    except Exception as e:
        return {"status": False, "details": f"Error checking sleep timeout: {e}"}
def check_macos_sleep():
    try:
        output = subprocess.check_output(['pmset', '-g'], text=True)
        match = re.search(r'sleep\s+(\d+)', output)
        if match:
            minutes = int(match.group(1))
            status = minutes <= 10
            return {"status": status, "details": f"Sleep timeout set to {minutes} minutes"}
        else:
            return {"status": False, "details": "Sleep timeout not set or unlimited"}
    except Exception as e:
        return {"status": False, "details": f"Error checking sleep timeout: {e}"}

def check_linux_sleep():
    try:
        output = subprocess.check_output(['gsettings', 'get', 'org.gnome.desktop.session', 'idle-delay'], text=True).strip()
        seconds = int(output)
        minutes = seconds // 60
        status = minutes <= 10
        return {"status": status, "details": f"Idle delay set to {minutes} minutes"}
    except Exception as e:
        return {"status": False, "details": f"Error checking idle delay: {e}"}
