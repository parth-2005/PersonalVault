# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Guide

### Current Project State
- `shulker_box/`: Flutter client scaffold.
- `desktop/`: Target for Python desktop app (currently empty).
- `landing_page/`: Target for landing page (currently empty).

### Flutter App Commands (`shulker_box/`)
- **Run**: `cd shulker_box && flutter run`
- **Test**: `cd shulker_box && flutter test`
- **Analyze**: `cd shulker_box && flutter analyze`
- **Build Android APK**: `cd shulker_box && flutter build apk`
- **Build iOS**: `cd shulker_box && flutter build ios`

---

# ShulkerBox — Master Project Context
> For use with AI coding assistants (Cursor, Copilot, Antigravity, etc.)
> Last updated: June 2026

---

## 1. What Is ShulkerBox?

ShulkerBox is a **zero-setup, self-hosted personal cloud storage ecosystem**. It lets non-technical users share and transfer files directly between their own devices — PC to PC, and PC to Android — over an encrypted peer-to-peer mesh network powered by Tailscale.

**Core philosophy:** No public cloud. No monthly subscription. No IT knowledge required. You own your files, your network, your data.

**Name origin:** Minecraft's Shulker Box — a container that stores your items and teleports with you. Same concept: your stuff follows you, everywhere, privately.

**Tagline:** *"Your files. Your network. No cloud required."*

---

## 2. Target User

- Non-technical individuals (students, families, small freelancers)
- People who are tired of paying for Google Drive / iCloud / Dropbox
- People who care about privacy but don't want to self-host something complex
- Age range: 18–45, moderate tech comfort (can install an app, not a sysadmin)

**Design principle:** If the user has to open a terminal, we failed.

---

## 3. System Architecture (High Level)

```
[ PC Node A ]  <----Tailscale WireGuard Tunnel---->  [ PC Node B ]
     |                                                      |
  WsgiDAV                                               WsgiDAV
  Server                                                 Server
  (Python)                                              (Python)
     |                                                      |
  ShulkerBox                                           ShulkerBox
  Desktop App                                          Desktop App
  (System Tray)                                        (System Tray)
```

Later phase:
```
[ PC Node ]  <----Tailscale Tunnel---->  [ Android App (Flutter) ]
```

**Three-layer stack:**
- **Networking:** Tailscale (tsnet) — zero-config NAT traversal, WireGuard encryption
- **Protocol:** WebDAV over HTTP — directory listing, streaming, chunked upload/download
- **Application:** Python (desktop daemon) + Flutter (Android client, future)

---

## 4. MVP Scope — Two Deliverables

### Deliverable 1: PC ↔ PC (Current Sprint)
- Works on **Linux and Windows**
- User installs ShulkerBox desktop app
- App runs silently as a **system tray application**
- Automatically starts a WsgiDAV server bound to the Tailscale network interface
- Other PC on the same Tailnet can browse and transfer files through ShulkerBox UI
- Zero terminal usage. Zero manual firewall config. Zero IP lookup.

### Deliverable 2: PC ↔ Android (Next Sprint)
- Flutter Android app
- Connects to PC's ShulkerBox over Tailnet
- Browse, upload, download files
- Native Android share sheet integration ("Send to ShulkerBox")
- Background auto-backup of DCIM folder when Tailnet is active

---

## 5. Desktop App — Full Specification

### 5a. Tech Stack
- **Language:** Python 3.10+
- **WebDAV Server:** `WsgiDAV` library
- **Tailscale Integration:** Tailscale CLI (must be installed separately — we detect and guide, not bundle)
- **System Tray:** `pystray` (cross-platform tray icon)
- **UI Framework:** `tkinter` (for settings popup only — minimal, not a full window)
- **Packaging:** PyInstaller → single `.exe` (Windows) and single binary (Linux)
- **Config Storage:** JSON file in user's home directory (`~/.shulkerbox/config.json`)

### 5b. Behavior on Launch
1. App starts silently — no window, only a tray icon
2. Checks if Tailscale is installed and running
   - If not: shows a one-time friendly notification with a link to tailscale.com/download
3. Detects the machine's Tailscale IP (runs `tailscale ip -4` internally)
4. Starts WsgiDAV server bound to that Tailscale IP on port `8765`
5. Tray icon shows green dot = connected, grey dot = Tailscale not active
6. Right-click tray menu:
   - "Open Shared Folder" → opens the shared directory in native file explorer
   - "My Tailscale IP" → copies IP to clipboard with a toast notification
   - "Settings" → opens minimal settings popup
   - "Quit ShulkerBox"

### 5c. Settings Popup (tkinter window)
Fields:
- Shared Folder Path (directory picker)
- Port (default: 8765)
- Start on login toggle (adds to startup)
- Optional: username/password for WebDAV auth (blank = no auth, fine for home networks)

### 5d. File Structure (Python Project)
```
shulkerbox-desktop/
├── main.py                  # Entry point, tray setup
├── server.py                # WsgiDAV configuration and server lifecycle
├── tailscale.py             # Tailscale detection, IP fetching, status polling
├── config.py                # Read/write config.json
├── ui/
│   ├── tray.py              # pystray menu definition
│   └── settings_window.py  # tkinter settings popup
├── assets/
│   ├── icon_active.png      # Tray icon — green state
│   └── icon_inactive.png    # Tray icon — grey state
├── requirements.txt
├── build_windows.spec       # PyInstaller spec for Windows
├── build_linux.spec         # PyInstaller spec for Linux
└── README.md
```

### 5e. server.py — WsgiDAV Config
```python
# Key configuration points for WsgiDAV:
# - Root path: user's configured shared folder
# - Host: Tailscale IP only (NOT 0.0.0.0 — security requirement)
# - Port: 8765 (configurable)
# - Auth: optional digest auth if user sets credentials
# - Directory browsing: enabled
# - Chunked transfer: enabled (for large file support)
# - CORS: disabled (not a web app)
```

### 5f. tailscale.py — Key Functions Needed
```python
def is_tailscale_installed() -> bool
def is_tailscale_running() -> bool
def get_tailscale_ip() -> str | None       # runs: tailscale ip -4
def get_tailscale_status() -> dict          # runs: tailscale status --json
def poll_tailscale_status(callback, interval=10)  # background thread poller
```

### 5g. Cross-Platform Notes
| Concern | Windows | Linux |
|---|---|---|
| Tailscale detection | Check `%PROGRAMFILES%\Tailscale` or `where tailscale` | `which tailscale` |
| Start on login | Add to `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` | Add `.desktop` file to `~/.config/autostart/` |
| Open folder | `os.startfile(path)` | `xdg-open path` |
| Tray icon | pystray works natively | pystray needs `libappindicator` on some distros |
| Packaging | PyInstaller → `.exe` | PyInstaller → binary, optionally wrap in `.deb` |

---

## 6. Landing Page — Full Specification

### 6a. Purpose
- Present ShulkerBox as a real product
- Collect emails for "Pioneer Access" (our early tester program)
- Communicate value clearly to non-technical users
- Build trust: open source, privacy-first, no cloud

### 6b. Sections
1. **Hero** — Headline, subheadline, email signup CTA
2. **The Problem** — "You pay every month just to store your own files on someone else's server"
3. **How It Works** — 3-step visual: Install → Connect → Done
4. **Features** — 4 cards: Zero Setup, End-to-End Encrypted, No Subscription, Works Everywhere
5. **Pioneer Access** — Early tester signup section (email + optional: what device are you on?)
6. **Footer** — GitHub link, tagline, no tracking disclaimer

### 6c. Design Direction
- **Aesthetic:** Dark theme. Terminal/mesh network inspired. Not gamer. Think "sophisticated hacker tool made friendly."
- **Color palette:** Deep dark backgrounds (#0D0D0D or #0F1117), accent color is a warm amber/gold (#F5A623) for CTAs and highlights, white for primary text, muted grey for secondary
- **Typography:** Monospace font for code-like elements and the product name. Clean sans-serif for body. Example pairing: `JetBrains Mono` (headings/brand) + `Inter` or `DM Sans` (body)
- **Animations:** Subtle. Mesh/network lines in the background of the hero. Nodes connecting — like Tailscale's own visual metaphor.
- **No stock photos.** SVG illustrations or pure CSS/canvas visuals only.
- **Mobile responsive:** Yes, fully.

### 6d. Pioneer Access Form
Fields:
- Email (required)
- "What will you use ShulkerBox for?" — dropdown: Personal file sync / Family sharing / Work between my own machines / Just curious
- Submit button: "Join the Pioneers"

On submit:
- For now: POST to a simple serverless function (Netlify Forms, Formspree, or Supabase — pick one)
- Show thank you message: *"You're in. We'll reach out when Pioneer Access opens."*

### 6e. Tech Stack for Landing Page
- Pure HTML + CSS + Vanilla JS (no frameworks — keeps it fast and simple to deploy)
- Deploy to: Netlify (free tier, custom domain ready)
- No cookies, no analytics (we say this explicitly on the page — it builds trust)

---

## 7. Milestone Tracker

| Milestone | Description | Status |
|---|---|---|
| M0 | Project scaffolding + PRD | ✅ Done |
| M1 | Landing page live | 🔲 In progress |
| M2 | PC↔PC local Wi-Fi (no Tailscale yet) | 🔲 Next |
| M3 | PC↔PC over Tailnet (cross-network) | 🔲 Planned |
| M4 | Android Flutter client MVP | 🔲 Planned |
| M5 | Android share intent + background backup | 🔲 Planned |
| M6 | Google Play closed testing | 🔲 Planned |

---

## 8. Naming & Branding

- **Product name:** ShulkerBox
- **Tagline:** "Your files. Your network. No cloud required."
- **Early tester program name:** Pioneer Access
- **GitHub org (suggested):** `shulkerbox-app`
- **Domain (suggested):** `shulkerbox.app` or `shulker.box` (check availability)
- **Logo concept:** A Minecraft-esque box/container, but minimal and geometric — not pixel art. Think: a simple cube wireframe with a subtle mesh/network dot pattern.

---

## 9. What We Are NOT Building (Scope Guard)

- No custom VPN — we use Tailscale
- No custom protocol — we use WebDAV
- No web portal to access files from a browser (V2 feature)
- No team collaboration features (V2)
- No file versioning (V2)
- No iOS app in MVP
- We are NOT bundling Tailscale — user installs it separately, we detect and guide

---

## 10. Key Dependencies

```
# Python (desktop)
wsgidav>=4.3.0
cheroot>=9.0.0        # WSGI server that WsgiDAV runs on
pystray>=0.19.0
Pillow>=10.0.0        # Required by pystray for icons
pyinstaller>=6.0.0    # Packaging

# Flutter (Android - future sprint)
webdav_client: ^0.3.0
workmanager: ^0.5.0
receive_sharing_intent: ^1.8.0
```
