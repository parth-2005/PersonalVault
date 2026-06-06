import sys
import threading
import tkinter as tk
from typing import Dict, Any, Optional

import config
import tailscale
import server
from ui.tray import create_tray_icon
from ui.settings_window import show_settings_window

VERSION = "0.1.0"

class ShulkerBoxApp:
    def __init__(self):
        self.config = config.load_config()
        self.tailscale_ip: Optional[str] = None
        self.is_connected = False
        self.server_thread = None
        self.root = tk.Tk()
        self.root.withdraw() # Hide the main tkinter window

    def get_tray_status(self) -> Dict[str, Any]:
        """Returns current status for the tray icon."""
        return {
            "active": self.is_connected,
            "ip": self.tailscale_ip,
            "shared_folder": self.config.get("shared_folder_path", "")
        }

    def on_tailscale_status_change(self, active: bool, ip: Optional[str]) -> None:
        """Handler called by the Tailscale poller."""
        self.is_connected = active
        self.tailscale_ip = ip

        if active and ip:
            print(f"Tailscale connected: {ip}. Starting server...")
            self.start_webdav_server(ip)
        else:
            print("Tailscale disconnected. Stopping server...")
            server.stop_server()

    def start_webdav_server(self, ip: str) -> None:
        """Starts the WebDAV server using current config."""
        # Ensure server is not already running
        if server.is_server_running():
            return

        self.server_thread = server.start_server(
            host=ip,
            port=self.config.get("port", 8765),
            shared_folder=self.config.get("shared_folder_path", ""),
            username=self.config.get("webdav_username"),
            password=self.config.get("webdav_password")
        )

    def open_settings(self) -> None:
        """Opens the settings popup window."""
        def on_save(new_config):
            self.config = new_config
            config.save_config(new_config)
            # If server is running, restart it to apply new port/folder/auth
            if self.is_connected and self.tailscale_ip:
                server.stop_server()
                self.start_webdav_server(self.tailscale_ip)

        show_settings_window(self.config, on_save)

    def quit_app(self) -> None:
        """Cleans up and exits the application."""
        print("Quitting ShulkerBox...")
        server.stop_server()
        self.root.quit()
        sys.exit(0)

    def run(self) -> None:
        """Starts the application lifecycle."""
        # 1. Check Tailscale installation
        if not tailscale.is_tailscale_installed():
            print("Tailscale not installed. Please visit tailscale.com/download")
            # In a real app, we'd use a system notification here.
            # For MVP, we'll just print.
            # We could also use webbrowser.open("https://tailscale.com/download")

        # 2. Start Tailscale polling in background
        tailscale.poll_tailscale_status(self.on_tailscale_status_change)

        # 3. Run system tray (this is blocking)
        create_tray_icon(
            on_settings_click=self.open_settings,
            on_quit=self.quit_app,
            get_status=self.get_tray_status
        )

def main() -> None:
    app = ShulkerBoxApp()
    app.run()

if __name__ == "__main__":
    main()
