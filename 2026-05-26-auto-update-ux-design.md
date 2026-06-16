# Auto-Update UX — Design Spec

## Goal
Give the Tauri desktop app a working auto-update UX: check for updates, notify the user, and install with minimal friction.

## Architecture
```
Codeberg Pages (releases.json) ──HTTP──> Tauri Desktop (startup + manual check)
                                          │
                                   ┌──────┴──────┐
                                   │ updater.rs   │
                                   │ - check_for_updates
                                   │ - install_update
                                   │ - get_current_version
                                   └──────────────┘
                                          │
                                   ┌──────┴──────┐
                                   │ tray.rs      │
                                   │ - "Check for Updates" item
                                   │ - "Update Available" item
                                   └──────────────┘
                                          │
                                   ┌──────┴──────┐
                                   │ bridge       │
                                   │ - listen("update-checked")
                                   │ → toast notification
                                   └──────────────┘
```

## Components

### releases.json (Codeberg Pages)
Hosted at `https://world-office.codeberg.page/desktop-releases/releases.json`:
```json
{
  "latest_version": "1.2.3",
  "download_url": "https://codeberg.org/World-Office/desktop-releases/releases/download/v1.2.3/world-office_1.2.3_amd64.deb",
  "release_notes_url": "https://codeberg.org/World-Office/server/releases/tag/v1.2.3",
  "checksum_sha256": "abcdef..."
}
```
Updated manually per release. Linux `.deb` only (tracking Option B scope).

### updater.rs
- `get_current_version()` — compile-time `env!("CARGO_PKG_VERSION")`
- `check_for_updates()` — async `reqwest` GET to releases.json, parse, semver compare via `semver` crate. Returns `UpdateInfo { available: bool, version: Option<String>, download_url: Option<String> }`
- `install_update(url)` — download to `tempdir`, verify sha256, run `xdg-open` or `dpkg -i`, or spawn detached installer process
- Emits Tauri events: `update-checked`, `update-downloaded`, `update-error`

### tray.rs additions
- Insert "Check for Updates" menu item
- When update available: replace with "Update Available — Install Now" (bold/emphasized)
- Maintain a `Arc<AtomicBool>` state for update availability

### commands.rs additions
- `trigger_update_check` — runs `check_for_updates`, returns result, emits event
- `install_pending_update` — runs `install_update` with stored URL

### Frontend bridge
- `bridge/event-listener.ts`: add `listen("update-checked")` → dispatch DOM event `wo:update-checked`
- `App.tsx`: listener shows inline toast for 8s: "World Office X.Y.Z available — [Install] [Dismiss]"

### Dependencies
- `reqwest` with `rustls-tls` feature (already in workspace)
- `semver` crate (new)
- `sha2` crate (new, for checksum verification)
- `tempfile` crate (new, for download temp dir)

## Testing
- Unit test: `get_current_version` returns non-empty string
- Unit test: `check_for_updates` handles network error gracefully (returns `available: false`)
- Manual test: launch app, check tray menu has "Check for Updates"

## Out of Scope (Phase 2)
- Auto-download in background
- Install on quit (like Chrome)
- macOS/Windows installers
- Release notes panel
