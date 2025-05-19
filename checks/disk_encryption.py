import platform
import subprocess

def check_disk_encryption():
    system = platform.system()
    if system == "Windows":
        return check_bitlocker_status()
    elif system == "Darwin":  # macOS
        return check_filevault_status()
    elif system == "Linux":
        return check_luks_status()
    else:
        return {"status": False, "details": f"Unsupported OS: {system}"}

def check_bitlocker_status():
    try:
        output = subprocess.check_output(
            ["manage-bde", "-status", "C:"],
            stderr=subprocess.STDOUT,
            text=True
        )
        if "Conversion Status: Fully Encrypted" in output:
            return {"status": True, "details": "BitLocker fully encrypted"}
        else:
            return {"status": False, "details": "BitLocker not fully encrypted or disabled"}
    except subprocess.CalledProcessError as e:
        if e.returncode == 2147749891:
            return {"status": False, "details": "Requires admin privileges to check BitLocker status"}
        return {"status": False, "details": f"Error checking BitLocker: {e}"}
    except Exception as e:
        return {"status": False, "details": f"Unexpected error: {e}"}

def check_filevault_status():
    try:
        output = subprocess.check_output(
            ["fdesetup", "status"],
            stderr=subprocess.STDOUT,
            text=True
        )
        if "FileVault is On" in output:
            return {"status": True, "details": "FileVault enabled"}
        else:
            return {"status": False, "details": "FileVault is Off"}
    except Exception as e:
        return {"status": False, "details": f"Error checking FileVault: {e}"}

def check_luks_status():
    try:
        output = subprocess.check_output(
            ["lsblk", "-o", "NAME,TYPE,MOUNTPOINT"],
            stderr=subprocess.STDOUT,
            text=True
        )
        # Simple check if crypt device exists and is mounted at root
        if "crypt" in output:
            return {"status": True, "details": "LUKS encryption detected"}
        else:
            return {"status": False, "details": "No LUKS encryption detected"}
    except Exception as e:
        return {"status": False, "details": f"Error checking LUKS: {e}"}
