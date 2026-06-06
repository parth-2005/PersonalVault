# 📦 ShulkerBox Desktop

**Your files. Your network. No cloud required.**

ShulkerBox is a zero-setup, self-hosted personal cloud storage ecosystem. It allows you to share and transfer files directly between your own devices (PC to PC, and eventually PC to Android) over an encrypted peer-to-peer mesh network powered by Tailscale.

Unlike traditional cloud storage, ShulkerBox doesn't use a central server. Your data never leaves your hands—it moves directly from one of your devices to another.

## ✨ Features

- **Zero Configuration**: No router port-forwarding, no static IPs, and no complex firewall rules.
- **Privacy-First**: End-to-end encryption via Tailscale (WireGuard).
- **Seamless Integration**: Runs silently in your system tray.
- **Instant Sharing**: One click to open your shared folder or copy your Tailscale IP.
- **Cross-Platform**: Works natively on Windows and Linux.
- **No Subscriptions**: Completely free and self-hosted.

## 🛠️ Architecture

ShulkerBox creates a bridge between the **Tailscale** mesh network and your local filesystem using the **WebDAV** protocol.

1. **Networking**: Tailscale handles NAT traversal and encryption.
2. **Protocol**: A `WsgiDAV` server provides the file-sharing interface.
3. **Application**: A Python daemon manages the server lifecycle and provides a system tray UI via `pystray`.

## 🚀 Getting Started

### Prerequisites

**Tailscale** must be installed and running on all devices you wish to connect.
👉 [Download Tailscale](https://tailscale.com/download)

### Installation (Development)

1. **Clone the repository** and navigate to the desktop folder:
   ```bash
   cd desktop
   ```

2. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # OR
   .\venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

Start the application:
```bash
python main.py
```

The app will start silently. Look for the **ShulkerBox icon** in your system tray.

## ⚙️ Configuration

Right-click the tray icon and select **Settings** to configure:
- **Shared Folder**: The directory on your PC that other devices can access.
- **Port**: The port the WebDAV server listens on (Default: `8765`).
- **Start on Login**: Automatically launch ShulkerBox when you start your computer.
- **Authentication**: Optional username and password to protect your shared folder.

## 📦 Packaging & Distribution

ShulkerBox uses **PyInstaller** to bundle the application into a single executable.

### Using the Makefile

We provide a `Makefile` to simplify the build process:

- **Build for Windows**:
  ```bash
  make build-windows
  ```
- **Build for Linux**:
  ```bash
  make build-linux
  ```
- **Clean build artifacts**:
  ```bash
  make clean
  ```

The resulting binaries will be located in the `dist/` folder.

## 📂 Project Structure

```text
desktop/
├── main.py                # Application entry point & lifecycle manager
├── config.py              # Configuration management (~/.shulkerbox/config.json)
├── tailscale.py           # Tailscale API wrapper and status poller
├── server.py              # WsgiDAV & Cheroot server implementation
├── ui/
│   ├── tray.py            # System tray menu and icon logic
│   └── settings_window.py # Tkinter-based settings popup
├── assets/                # Tray icons (active/inactive)
└── requirements.txt       # Python dependencies
```

## 📜 License

This project is open source. See the LICENSE file for details.
