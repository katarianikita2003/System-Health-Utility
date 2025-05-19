import platform
import subprocess

def check_antivirus():
    system = platform.system()
    if system == "Windows":
        return check_windows_antivirus()
    elif system == "Darwin":
        return check_macos_antivirus()
    elif system == "Linux":
        return check_linux_antivirus()
    else:
        return {"status": False, "details": f"Unsupported OS: {system}"}

def check_windows_antivirus():
    try:
        cmd = ['powershell', '-Command', 'Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct | Select-Object displayName,productState']
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        if output.strip() == "":
            return {"status": False, "details": "No antivirus products detected"}
        else:
            return {"status": True, "details": output.strip()}
    except Exception as e:
        return {"status": False, "details": f"Error checking antivirus: {e}"}

def check_macos_antivirus():
    # macOS does not have built-in AV, so check for common AV apps running (basic)
    common_av = ["Symantec", "McAfee", "Norton", "Avast", "Sophos", "Trend Micro"]
    try:
        output = subprocess.check_output(['ps', 'aux'], text=True)
        found = [av for av in common_av if av.lower() in output.lower()]
        if found:
            return {"status": True, "details": f"Antivirus detected: {', '.join(found)}"}
        else:
            return {"status": False, "details": "No antivirus detected"}
    except Exception as e:
        return {"status": False, "details": f"Error checking antivirus: {e}"}

def check_linux_antivirus():
    # Check for common AV processes on Linux
    common_av = ["clamd", "freshclam", "clamav", "chkrootkit"]
    try:
        output = subprocess.check_output(['ps', 'aux'], text=True)
        found = [av for av in common_av if av.lower() in output.lower()]
        if found:
            return {"status": True, "details": f"Antivirus detected: {', '.join(found)}"}
        else:
            return {"status": False, "details": "No antivirus detected"}
    except Exception as e:
        return {"status": False, "details": f"Error checking antivirus: {e}"}
