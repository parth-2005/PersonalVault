import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Callable, Dict

def show_settings_window(initial_config: dict, on_save: Callable[[dict], None]) -> None:
    """
    Creates and displays the minimal settings popup window.
    """
    window = tk.Toplevel()
    window.title("ShulkerBox Settings")
    window.geometry("450x350")
    window.resizable(False, False)
    window.configure(bg="#1e1e1e")

    # Center window on screen
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"+{x}+{y}")

    # Style
    bg_color = "#1e1e1e"
    fg_color = "#ffffff"
    accent_color = "#F5A623"

    # Layout helper
    def create_label(text):
        return tk.Label(window, text=text, bg=bg_color, fg=fg_color, font=("Arial", 10))

    # --- Shared Folder ---
    tk.Label(window, text="Shared Folder", bg=bg_color, fg=fg_color, font=("Arial", 10, "bold")).pack(pady=(20, 5))
    folder_frame = tk.Frame(window, bg=bg_color)
    folder_frame.pack(fill="x", padx=40)

    folder_var = tk.StringVar(value=initial_config.get("shared_folder_path", ""))
    folder_entry = tk.Entry(folder_frame, textvariable=folder_var, bg="#2d2d2d", fg=fg_color, insertbackground=fg_color)
    folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

    def browse_folder():
        path = filedialog.askdirectory()
        if path:
            folder_var.set(path)

    tk.Button(folder_frame, text="Browse", command=browse_folder, bg="#3d3d3d", fg=fg_color).pack(side="right")

    # --- Port ---
    tk.Label(window, text="Port", bg=bg_color, fg=fg_color, font=("Arial", 10, "bold")).pack(pady=(15, 5))
    port_var = tk.StringVar(value=str(initial_config.get("port", 8765)))
    port_entry = tk.Entry(window, textvariable=port_var, bg="#2d2d2d", fg=fg_color, insertbackground=fg_color, justify="center")
    port_entry.pack()

    # --- Start on Login ---
    start_on_login_var = tk.BooleanVar(value=initial_config.get("start_on_login", False))
    tk.Checkbutton(window, text="Start on login", variable=start_on_login_var, bg=bg_color, fg=fg_color, selectcolor="#000000", activebackground=bg_color, activeforeground=fg_color).pack(pady=15)

    # --- Credentials ---
    tk.Label(window, text="WebDAV Credentials (Optional)", bg=bg_color, fg=fg_color, font=("Arial", 10, "bold")).pack(pady=(15, 5))

    user_var = tk.StringVar(value=initial_config.get("webdav_username", ""))
    tk.Entry(window, textvariable=user_var, bg="#2d2d2d", fg=fg_color, insertbackground=fg_color, justify="center").pack(pady=2)

    pass_var = tk.StringVar(value=initial_config.get("webdav_password", ""))
    pass_entry = tk.Entry(window, textvariable=pass_var, show="*", bg="#2d2d2d", fg=fg_color, insertbackground=fg_color, justify="center")
    pass_entry.pack(pady=2)

    def toggle_password():
        if pass_entry.cget("show") == "*":
            pass_entry.config(show="")
        else:
            pass_entry.config(show="*")

    tk.Button(window, text="Show/Hide Password", command=toggle_password, bg="#3d3d3d", fg=fg_color, font=("Arial", 8)).pack()

    # --- Buttons ---
    btn_frame = tk.Frame(window, bg=bg_color)
    btn_frame.pack(side="bottom", pady=30)

    def save_and_close():
        try:
            port = int(port_var.get())
            if not (1024 <= port <= 65535):
                raise ValueError("Port must be between 1024 and 65535")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        new_config = {
            "shared_folder_path": folder_var.get(),
            "port": port,
            "start_on_login": start_on_login_var.get(),
            "webdav_username": user_var.get(),
            "webdav_password": pass_var.get(),
        }
        on_save(new_config)
        window.destroy()

    tk.Button(btn_frame, text="Save", command=save_and_close, bg=accent_color, fg="#000000", font=("Arial", 10, "bold"), width=10).pack(side="left", padx=10)
    tk.Button(btn_frame, text="Cancel", command=window.destroy, bg="#3d3d3d", fg=fg_color, font=("Arial", 10), width=10).pack(side="right", padx=10)

    # Make modal
    window.grab_set()
