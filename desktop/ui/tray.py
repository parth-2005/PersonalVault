import os
import subprocess
import sys
import threading
from PIL import Image
import pystray
from pystray import MenuItem as Item
from typing import Callable, Dict, Any

def open_folder(path: str):
    """Opens the specified folder in the native file explorer."""
    if sys.platform == "win32":
        os.startfile(path)
    elif sys.platform == "darwin":
        subprocess.run(["open", path])
    else:
        subprocess.run(["xdg-open", path], check=False)

def copy_to_clipboard(text: str):
    """Copies the given text to the system clipboard."""
    if sys.platform == "win32":
        subprocess.run(["clip"], input=text.encode("utf-8"), check=True)
    elif sys.platform == "darwin":
        subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)
    else:
        try:
            subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode("utf-8"), check=True)
        except FileNotFoundError:
            subprocess.run(["xsel", "-i", "clipboard"], input=text.encode("utf-8"), check=True)

def create_tray_icon(on_settings_click: Callable[[], None], on_quit: Callable[[], None], get_status: Callable[[], Dict[str, Any]]) -> None:
    """
    Initializes and runs the system tray application using pystray.
    """

    def get_icon():
        status = get_status()
        # Load icons from assets folder. Fallback to a solid color if not found.
        try:
            if status.get("active"):
                return Image.open("assets/icon_active.png")
            else:
                return Image.open("assets/icon_inactive.png")
        except Exception:
            # Create a simple colored square as fallback
            img = Image.new('RGB', (64, 64), color=(0, 255, 0) if status.get("active") else (128, 128, 128))
            return img

    def make_menu(status):
        # Build a fresh menu based on the provided status snapshot
        status_label = f"● Connected — {status.get('ip', 'Unknown')}" if status.get("active") else "○ Tailscale not active"
        return pystray.Menu(
            Item("ShulkerBox", lambda: None, enabled=False),
            pystray.Menu.SEPARATOR,
            Item(status_label, lambda: None, enabled=False),
            pystray.Menu.SEPARATOR,
            Item("Open Shared Folder", lambda: open_folder(status.get("shared_folder", ""))),
            Item("Copy My IP", lambda: copy_to_clipboard(status.get("ip", ""))),
            Item("Settings", on_settings_click),
            pystray.Menu.SEPARATOR,
            Item("Quit ShulkerBox", on_quit),
        )

    icon = pystray.Icon("ShulkerBox", icon=get_icon(), menu=make_menu(get_status()))

    def updater_loop(icon):
        # Background thread to periodically refresh icon and menu
        import time
        while True:
            try:
                status = get_status()
                icon.icon = get_icon()
                icon.menu = make_menu(status)
            except Exception:
                pass
            time.sleep(3)

    # Start updater thread before run so menu stays responsive
    updater = threading.Thread(target=lambda: updater_loop(icon), daemon=True)
    updater.start()

    # pystray doesn't have a built-in "timer" for updates.
    # We'll just update the icon when it's requested or in the main loop.
    # For simplicity here, we'll let the main loop handle status updates.

    # However, pystray's run() is blocking.
    icon.run()
