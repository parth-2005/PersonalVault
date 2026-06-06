# ShulkerBox — AI Assistant Prompts
> Copy-paste these into Cursor, Copilot, Antigravity, or any AI coding tool.
> Each prompt is self-contained. Feed PROJECT_CONTEXT.md as context first, then use the prompt.

---

## HOW TO USE THESE PROMPTS

1. Open your AI coding assistant
2. Attach or paste `PROJECT_CONTEXT.md` as context / system prompt
3. Use the prompts below one at a time, in order
4. Each prompt builds on the previous one

---

---
# BLOCK A: DESKTOP APP (Python)
---

## Prompt A1 — Project Scaffold

```
You are building the ShulkerBox desktop application. Read the PROJECT_CONTEXT.md I've provided.

Create the full project scaffold for the Python desktop app exactly as described in Section 5d of the context. Do the following:

1. Create all files and folders as specified in the file structure
2. Each file should have the correct imports and a clear docstring explaining its role
3. requirements.txt should include all dependencies from Section 10 with pinned minimum versions
4. main.py should be the entry point that initializes tray, config, and server in the correct order
5. Every file should have stub functions with proper type hints and docstrings — no implementation yet, just the skeleton

Do not implement logic yet. Just scaffold. Make it feel like a professional Python project from day one.
```

---

## Prompt A2 — Config Module

```
Context: ShulkerBox desktop app. See PROJECT_CONTEXT.md Section 5c and 5d.

Implement config.py fully. Requirements:
- Config is stored at ~/.shulkerbox/config.json
- Fields: shared_folder_path (str), port (int, default 8765), start_on_login (bool, default False), webdav_username (str, optional), webdav_password (str, optional)
- Functions: load_config() -> dict, save_config(config: dict), get_default_config() -> dict
- On first run, create ~/.shulkerbox/ directory and write default config
- Handle missing keys gracefully (merge with defaults on load)
- No third-party libraries — stdlib only (json, pathlib, os)
```

---

## Prompt A3 — Tailscale Module

```
Context: ShulkerBox desktop app. See PROJECT_CONTEXT.md Section 5f.

Implement tailscale.py fully. Requirements:

1. is_tailscale_installed() -> bool
   - Windows: check if 'tailscale.exe' exists in Program Files or is on PATH
   - Linux: check if 'tailscale' binary is on PATH using shutil.which

2. is_tailscale_running() -> bool
   - Run 'tailscale status' and check return code
   - Return False if command fails or times out (2s timeout)

3. get_tailscale_ip() -> str | None
   - Run 'tailscale ip -4'
   - Return IP string or None on failure
   - Strip whitespace from output

4. get_tailscale_status() -> dict
   - Run 'tailscale status --json'
   - Parse and return JSON, or return {'error': 'unavailable'} on failure

5. poll_tailscale_status(on_status_change: callable, interval: int = 10)
   - Background thread that polls every `interval` seconds
   - Calls on_status_change(is_active: bool, ip: str | None) when status changes
   - Must handle thread cleanup gracefully on app exit

Cross-platform: use subprocess with shell=False. Handle timeouts. No hardcoded paths.
```

---

## Prompt A4 — WebDAV Server Module

```
Context: ShulkerBox desktop app. See PROJECT_CONTEXT.md Section 5e.

Implement server.py fully using WsgiDAV + Cheroot. Requirements:

1. start_server(host: str, port: int, shared_folder: str, username: str = None, password: str = None) -> threading.Thread
   - Configure WsgiDAV with the shared_folder as root
   - Bind ONLY to the provided host IP (not 0.0.0.0 — this is a security requirement)
   - If username and password are provided, enable HTTP Digest authentication
   - If not, disable auth entirely
   - Enable directory browsing
   - Start Cheroot WSGI server in a daemon thread
   - Return the thread

2. stop_server()
   - Gracefully stop the Cheroot server

3. is_server_running() -> bool

4. get_server_url(host: str, port: int) -> str
   - Returns e.g. "http://100.x.y.z:8765"

The server must NOT crash the main app if it fails to bind. Catch exceptions, log them, and surface an error state instead.
```

---

## Prompt A5 — System Tray

```
Context: ShulkerBox desktop app. See PROJECT_CONTEXT.md Section 5b and 5g.

Implement ui/tray.py using pystray. Requirements:

The tray icon should:
1. Show icon_active.png when Tailscale is connected and server is running
2. Show icon_inactive.png when Tailscale is offline

Right-click menu items:
- "ShulkerBox" (title, disabled/grayed) 
- Separator
- "● Connected — 100.x.y.z" OR "○ Tailscale not active" (dynamic status line, not clickable)
- Separator  
- "Open Shared Folder" → opens the shared folder in native file explorer
  - Windows: os.startfile(path)
  - Linux: subprocess.run(['xdg-open', path])
- "Copy My IP" → copies Tailscale IP to clipboard, shows a toast/notification "IP copied!"
- "Settings" → calls a callback to open the settings window
- Separator
- "Quit ShulkerBox" → cleanly stops server, stops tray

The tray must run on the main thread (pystray requirement). All other logic runs in background threads.

Accept these constructor args: on_settings_click: callable, on_quit: callable, get_status: callable -> dict
```

---

## Prompt A6 — Settings Window

```
Context: ShulkerBox desktop app. See PROJECT_CONTEXT.md Section 5c.

Implement ui/settings_window.py using tkinter. Requirements:

Create a clean, minimal settings window (not resizable, centered on screen, ~450x350px):

Fields:
1. Shared Folder — text field + "Browse" button that opens a native directory picker
2. Port — number field (default 8765, validate: must be 1024-65535)
3. Start on login — checkbox
4. Username — text field (optional, placeholder: "Leave blank for no auth")
5. Password — text field with show/hide toggle (optional)

Buttons:
- "Save" — validates, saves config, shows "Saved!" briefly, closes window
- "Cancel" — closes without saving

The window should:
- Open centered on screen
- Be modal (grab focus, prevent interacting with other windows)
- Pre-populate fields from current config on open
- Handle start-on-login cross-platform (Section 5g of context)

Style: Use a dark grey background (#1e1e1e) with white text to match ShulkerBox's dark aesthetic.
```

---

## Prompt A7 — Main Entry Point + Wiring

```
Context: ShulkerBox desktop app. See PROJECT_CONTEXT.md Section 5b.

Implement main.py — the entry point that wires everything together.

Startup sequence:
1. Load config (config.py)
2. Check if Tailscale is installed → if not, show a system notification: "ShulkerBox needs Tailscale. Visit tailscale.com/download" and open the URL
3. Start polling Tailscale status in background (tailscale.py)
4. When Tailscale IP is detected, start WsgiDAV server (server.py) bound to that IP
5. Start system tray (ui/tray.py) on main thread

Status change handler:
- When Tailscale connects: start server, update tray to active icon
- When Tailscale disconnects: stop server, update tray to inactive icon

Quit handler:
- Stop server
- Stop Tailscale poller thread
- Stop tray

The app must handle being run on both Windows and Linux without any code changes. Use sys.platform checks where needed.

Also add: if __name__ == '__main__': guard, and a VERSION = "0.1.0" constant at the top.
```

---

## Prompt A8 — PyInstaller Packaging

```
Context: ShulkerBox desktop app.

Create two PyInstaller spec files for packaging ShulkerBox into a single executable.

build_windows.spec:
- Single file executable (.exe)
- Include assets/ folder (both PNG icons)
- App name: ShulkerBox
- Icon: assets/icon_active.png (convert to .ico first in the spec)
- Hide console window (windowed=True)
- UPX compression if available

build_linux.spec:
- Single file binary
- Include assets/ folder
- App name: shulkerbox (lowercase for Linux convention)
- No console window

Also create a Makefile with:
- make build-windows
- make build-linux  
- make clean

And a GitHub Actions workflow file (.github/workflows/build.yml) that:
- On push to main: builds both Windows and Linux binaries
- Uploads them as release artifacts
- Uses windows-latest and ubuntu-latest runners
```

---
# BLOCK B: LANDING PAGE
---

## Prompt B1 — Landing Page (Complete, Single File)

```
You are building the ShulkerBox landing page. Read the PROJECT_CONTEXT.md I've provided, specifically Section 6.

Build a complete, single-file HTML landing page (HTML + CSS + JS all in one file). 

DESIGN DIRECTION (from Section 6c):
- Dark theme. Deep backgrounds: #0D0D0D base, #111318 for cards/sections
- Accent: warm amber/gold #F5A623 for CTAs and highlights
- Typography: JetBrains Mono (Google Fonts) for brand name and monospace accents. DM Sans for all body text
- Hero background: SVG canvas with animated mesh/network — nodes (dots) connected by faint lines, slowly animating. Subtle, not distracting. This is the KEY visual.
- No stock photos. No gradients (except very subtle on the hero backdrop). No purple. No glassmorphism.
- Feels like a sophisticated developer tool, made accessible.

SECTIONS (in order):
1. NAVBAR — Logo (ShulkerBox in JetBrains Mono), "Pioneer Access" CTA button (amber, right side)

2. HERO — 
   Headline: "Your files. Your network. No cloud required."
   Subheadline: "ShulkerBox connects your devices directly — no middleman, no subscription, no data leaving your hands."
   CTA: Email input + "Join Pioneer Access" button
   Below CTA: small social proof text "Be among the first 100 Pioneers"
   Background: animated mesh network SVG

3. THE PROBLEM — 
   Section headline: "You're renting access to your own files."
   3 pain point cards: "Pay monthly forever", "Your data on their servers", "Speed limited by their infrastructure"
   Each card has an icon, short headline, 1-sentence description.

4. HOW IT WORKS — 
   3 steps, horizontal on desktop, vertical on mobile:
   Step 1: Install ShulkerBox → Step 2: Add your devices → Step 3: Access everything
   Each step has a number, title, and 2-line description.
   Connecting line/arrow between steps.

5. FEATURES — 
   4 feature cards in a 2x2 grid:
   - Zero Setup (icon: plug) — "Install and go. No router config, no port forwarding, no IT degree needed."
   - End-to-End Encrypted (icon: lock) — "WireGuard encryption. Your files never touch a third-party server."
   - No Subscription (icon: slash through dollar sign) — "Free forever. Self-hosted. The only cost is your own hardware."
   - Works Everywhere (icon: globe/network) — "PC to PC. PC to phone. Home network or across the world."

6. PIONEER ACCESS —
   Full-width dark section with amber accent border
   Headline: "Become a Pioneer"
   Subheadline: "We're opening early access to a small group of testers. Help shape ShulkerBox before it launches."
   Form:
   - Email input
   - Dropdown: "What will you use ShulkerBox for?" [Personal file sync / Family sharing / My own machines / Just curious]
   - Submit: "Join the Pioneers →"
   On submit: hide form, show "You're in. We'll reach out when Pioneer Access opens." in amber text.
   Use Formspree action (placeholder URL: https://formspree.io/f/YOUR_FORM_ID — user will replace)

7. FOOTER —
   Logo + tagline
   Links: GitHub (placeholder #) | Privacy (one line: "We don't track you. No cookies. No analytics.")
   Bottom: "© 2026 ShulkerBox. Open source. Built for humans."

TECHNICAL REQUIREMENTS:
- Single .html file, no external CSS/JS files
- Google Fonts loaded via @import
- Formspree for form (no backend needed)
- Fully mobile responsive (hamburger menu not needed, just stack vertically)
- No jQuery, no frameworks — vanilla JS only
- Smooth scroll on nav links
- The mesh animation must be pure canvas/JS — no library

Make it look like a real funded startup landing page, not a hobby project.
```

---

## Prompt B2 — Landing Page Form Backend (Optional Upgrade)

```
Context: ShulkerBox Pioneer Access waitlist.

The landing page uses Formspree currently. I want to upgrade to a Supabase backend to store signups with timestamps and source tracking.

Create:
1. SQL schema for a `pioneers` table:
   - id (uuid, primary key)
   - email (text, unique, not null)
   - use_case (text) — from dropdown
   - signed_up_at (timestamptz, default now())
   - source (text, default 'landing_page')

2. A Supabase Edge Function (TypeScript) that:
   - Accepts POST with { email, use_case }
   - Validates email format
   - Inserts into pioneers table (handle duplicate gracefully — return success even if duplicate, don't leak whether email exists)
   - Returns { success: true } or { success: false, error: 'message' }

3. Updated JavaScript for the landing page form that:
   - POSTs to the Supabase Edge Function URL
   - Shows a loading spinner on the button while submitting
   - Handles success and error states
   - Rate limits client-side: disable button for 3s after click

Keep it simple. No email confirmation needed for MVP.
```

---
# BLOCK C: TESTING
---

## Prompt C1 — PC to PC Test Checklist Generator

```
Context: ShulkerBox MVP. Two PCs, both on the same Tailnet.

Generate a structured test plan for validating the PC ↔ PC file transfer. Include:

1. Pre-flight checks (Tailscale installed, both on same Tailnet, ShulkerBox running on both)
2. Basic connectivity test (can PC-B reach PC-A's WebDAV URL in browser?)
3. Directory listing test (does the shared folder appear correctly?)
4. Small file transfer test (<1MB)
5. Large file transfer test (>500MB — test chunking)
6. Network interruption test (disconnect Wi-Fi mid-transfer, reconnect — does it recover?)
7. Auth test (if credentials set, does wrong password correctly reject?)
8. Cross-OS test matrix: Windows→Windows, Linux→Linux, Windows→Linux, Linux→Windows

For each test: Expected result, Pass criteria, Failure notes to capture.

Format as a markdown checklist that a non-technical tester can follow.
```

---

## NOTES FOR YOUR AI ASSISTANT

- Always refer back to PROJECT_CONTEXT.md for architecture decisions
- The shared folder is NEVER 0.0.0.0 — always bind to Tailscale IP only
- The target user is non-technical — error messages must be human-readable, not stack traces
- When in doubt about UX, choose fewer clicks over more options
- We are NOT reinventing Tailscale or WebDAV — we are wrapping them for normal humans