import platform
import subprocess

def check_os_update():
    system = platform.system()
    if system == "Windows":
        return check_windows_update()
    elif system == "Darwin":  # macOS
        return check_macos_update()
    elif system == "Linux":
        return check_linux_update()
    else:
        return {"status": False, "details": f"Unsupported OS: {system}"}

def check_windows_update():
    try:
        cmd = ['powershell', '-Command', '(New-Object -ComObject Microsoft.Update.Session).CreateUpdateSearcher().Search("IsInstalled=0 and Type=\'Software\'").Updates.Count']
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True).strip()
        pending = int(output)
        if pending == 0:
            return {"status": True, "details": "No pending updates"}
        else:
            return {"status": False, "details": f"{pending} pending update(s)"}
    except Exception as e:
        return {"status": False, "details": f"Error checking Windows update: {e}"}

def check_macos_update():
    try:
        output = subprocess.check_output(
            ["softwareupdate", "-l"],
            stderr=subprocess.STDOUT,
            text=True
        )
        if "No new software available." in output:
            return {"status": True, "details": "No pending updates"}
        else:
            return {"status": False, "details": "Pending updates available"}
    except Exception as e:
        return {"status": False, "details": f"Error checking macOS update: {e}"}

def check_linux_update():
    try:
        output = subprocess.check_output(
            ["apt-get", "-s", "upgrade"],
            stderr=subprocess.STDOUT,
            text=True
        )
        if "0 upgraded" in output:
            return {"status": True, "details": "No pending updates"}
        else:
            return {"status": False, "details": "Pending updates available"}
    except Exception as e:
        return {"status": False, "details": f"Error checking Linux update: {e}"}
