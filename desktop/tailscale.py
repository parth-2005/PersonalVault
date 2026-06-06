import subprocess
import shutil
import json
import threading
import time
from typing import Dict, Optional, Callable, Any

def is_tailscale_installed() -> bool:
    """
    Checks if the Tailscale binary is installed on the current system.
    """
    # Check if 'tailscale' is in the system PATH
    if shutil.which("tailscale"):
        return True

    # Additional check for Windows Program Files if not in PATH
    import sys
    if sys.platform == "win32":
        import os
        # Common Tailscale install paths on Windows
        common_paths = [
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Tailscale"),
            os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Tailscale"),
        ]
        for path in common_paths:
            if os.path.exists(os.path.join(path, "tailscale.exe")):
                return True

    return False

def is_tailscale_running() -> bool:
    """
    Checks if the Tailscale daemon is currently running.
    """
    try:
        # 'tailscale status' returns non-zero if the daemon is not running
        subprocess.run(["tailscale", "status"], capture_output=True, check=True, timeout=2)
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return False

def get_tailscale_ip() -> Optional[str]:
    """
    Fetches the machine's current Tailscale IPv4 address.
    """
    try:
        result = subprocess.run(["tailscale", "ip", "-4"], capture_output=True, text=True, check=True, timeout=2)
        return result.stdout.strip()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return None

def get_tailscale_status() -> Dict[str, Any]:
    """
    Fetches detailed Tailscale status in JSON format.
    """
    try:
        result = subprocess.run(["tailscale", "status", "--json"], capture_output=True, text=True, check=True, timeout=2)
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
        return {"error": "unavailable"}

def poll_tailscale_status(on_status_change: Callable[[bool, Optional[str]], None], interval: int = 10) -> None:
    """
    Starts a background thread that polls Tailscale status every `interval` seconds.
    """
    def poller():
        last_status = (False, None) # (is_active, ip)

        while True:
            current_ip = get_tailscale_ip()
            current_active = current_ip is not None

            if (current_active, current_ip) != last_status:
                last_status = (current_active, current_ip)
                on_status_change(current_active, current_ip)

            time.sleep(interval)

    thread = threading.Thread(target=poller, daemon=True)
    thread.start()
