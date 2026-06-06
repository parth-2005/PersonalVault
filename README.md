# 📦 ShulkerBox

**Your files. Your network. No cloud required.**

ShulkerBox is a zero-setup, self-hosted personal cloud storage ecosystem. It enables private, encrypted file sharing and transfer between your own devices (PC to PC, and PC to Android) over a peer-to-peer mesh network powered by Tailscale.

No public cloud, no monthly subscriptions, and no complex IT knowledge required. You own your files, your network, and your data.

---

## 🚀 Core Components

### 🖥️ ShulkerBox Desktop (Python)
A system tray application that turns your PC into a private file server.
- **Automated Server**: Starts a WsgiDAV server bound exclusively to your Tailscale IP.
- **Zero Config**: Automatically detects your Tailscale status and IP.
- **Easy Management**: Quick access to your shared folder and connection settings via the system tray.
- **Cross-Platform**: Works on Windows and Linux.

### 📱 ShulkerBox Android (Flutter)
A mobile client to access your PC's files on the go.
- **Seamless Access**: Connect to your PC using its Tailscale IP.
- **File Management**: Browse, upload, and download files directly from your phone.
- **Native Integration**: Integrated with the Android share sheet ("Send to ShulkerBox").
- **Auto-Backup**: Background backup of your DCIM/Camera folder when connected to your Tailnet.

### 🌐 Landing Page
A professional product showcase and early-access portal for "Pioneer Access" testers.

---

## 🛠️ Tech Stack

- **Networking**: [Tailscale](https://tailscale.com) (WireGuard P2P Mesh)
- **Protocol**: WebDAV over HTTP
- **Desktop**: Python 3.10+, `WsgiDAV`, `pystray`, `tkinter`, `PyInstaller`
- **Mobile**: Flutter, `webdav_client`, `workmanager`, `receive_sharing_intent`
- **Web**: Vanilla HTML, CSS, and JavaScript

---

## 🏁 Getting Started

### Prerequisites
1. **Tailscale**: Install and log into Tailscale on all devices you wish to connect. This provides the secure "mesh" network that ShulkerBox uses.

### 1. Setting up the Desktop Server
1. Navigate to the `desktop/` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```
4. Right-click the tray icon $\rightarrow$ **Settings** to choose the folder you want to share.

### 2. Setting up the Android Client
1. Navigate to the `shulker_box/` directory.
2. Ensure you have the Flutter SDK installed.
3. Run the app on a connected device:
   ```bash
   flutter run
   ```
4. In the app, enter your PC's **Tailscale IP** (found by right-clicking the Desktop tray icon $\rightarrow$ "My Tailscale IP").

---

## 📂 Project Structure

```text
.
├── desktop/           # Python Desktop Application (Server)
├── shulker_box/       # Flutter Android Application (Client)
├── landing_page/      # Product Landing Page
├── AGENTS.md          # AI Agent instructions and project context
└── prompts.md         # Implementation prompts used for development
```

---

## 🧪 Development & Testing

### Desktop App
- **Build**: Use the provided `Makefile` to create standalone executables.
  ```bash
  make build-windows
  make build-linux
  ```

### Android App
- **Analyze**: `cd shulker_box && flutter analyze`
- **Test**: `cd shulker_box && flutter test`
- **Build APK**: `cd shulker_box && flutter build apk`

---

## 🛡️ Privacy & Security
ShulkerBox is designed with a **Privacy-First** approach:
- **No Third-Party Storage**: Your files never leave your devices.
- **End-to-End Encryption**: All traffic is encrypted via Tailscale's WireGuard tunnels.
- **Interface Binding**: The server binds only to the Tailscale IP, preventing exposure to the public internet.
