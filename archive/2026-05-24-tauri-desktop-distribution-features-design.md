# Tauri Desktop: Distribution Pipeline + Features — Design Spec

**Date:** 2026-05-24
**Status:** Complete (implemented in `desktop/tauri-poc/` and `.forgejo/workflows/desktop-release.yml`)
**Author:** Sisyphus

## Overview

The World-Office desktop shell uses Tauri 2.0 (Rust-based, FOSS-compliant, no CEF).
This spec covers two workstreams:

1. **Distribution Pipeline** — automated builds, Debian repository on Codeberg Pages, release workflow
2. **Desktop Features** — offline mode, settings window, plugin system, integration tests

## Platform Sequencing

### Phase 1 (Linux-only CI)
- Forgejo Actions builds on `ubuntu-24.04`
- Artifacts: .deb, AppImage, source tarball
- .deb published to Codeberg Pages Debian repository (apt-installable)
- GPG-signed Release files

### Phase 2 (Developer manual — future)
- macOS/Windows builds possible via `cargo tauri build` locally
- Developer certificate signing documented
- Requires self-hosted runners for CI enablement — not in Phase 1

## Distribution Pipeline

### CI Workflow

```
workflow: "Build & Publish Tauri Desktop"
  triggers:
    - tag: v*    → release build + publish
    - branch: main  → nightly build (optional: publish to nightly repo)

  job: build-linux
    runs-on: ubuntu-24.04
    steps:
      - actions/checkout@v4
      - apt install: libwebkit2gtk-4.1-dev, libappindicator3-dev,
                     librsvg2-dev, libssl-dev, pkg-config
      - setup: pnpm (--frozen-lockfile)
      - run: cd desktop/tauri-poc && cargo tauri build
      - sign .deb with GPG (secret: DEB_GPG_PRIVATE_KEY)
      - upload: world-office_*.deb, world-office_*.AppImage, world-office_*.tar.gz

  job: publish-debian-repo
    needs: build-linux
    runs-on: ubuntu-24.04
    steps:
      - download artifacts
      - sign repo Release file with GPG
      - add .deb to pool/
      - regenerate Packages.gz
      - push to Codeberg Pages Debian repo
```

### Debian Repository Structure

```
.debian/
├── dists/
│   └── stable/
│       ├── InRelease              # clearsigned Release
│       ├── Release                # unsigned metadata
│       ├── Release.gpg            # detached GPG sig
│       └── main/
│           └── binary-amd64/
│               ├── Packages       # package index
│               ├── Packages.gz    # compressed index
│               └── Release        # component-level metadata
└── pool/
    └── main/
        └── w/
            └── world-office_<version>_amd64.deb
```

### End-User Install

```sh
# Add repository key
sudo curl -fsSL https://pages.codeberg.org/world-office/debian/world-office.gpg \
  -o /usr/share/keyrings/world-office.gpg

# Add APT source
echo "deb [signed-by=/usr/share/keyrings/world-office.gpg] \
  https://pages.codeberg.org/world-office/debian stable main" \
  | sudo tee /etc/apt/sources.list.d/world-office.list

# Install
sudo apt update && sudo apt install world-office
```

### Repository Management

- **Codeberg repository**: `world-office/debian-repo`
- **Branch**: `pages` (Codeberg Pages convention — only this branch is published)
- **Domain**: `world-office.codeberg.page`
- **GPG key**: generated once, private key stored in Forgejo secret `DEB_GPG_PRIVATE_KEY`
- **Version tool**: `cargo bump` or manual tag — tag `v1.2.3` triggers workflow

## Desktop Features

### 1. Offline Mode

The Tauri shell already serves the same web app regardless of backend availability.
- **Local-only mode**: App connects to embedded local server (no external backend needed)
- **Storage**: `localStorage` + `IndexedDB` for document persistence
- **Sync toggle**: "Connect" button in toolbar when backend becomes available
- **No extra state machine**: rely on `navigator.onLine` + backend health check
- **Scope**: displays "Offline" badge, documents persist locally, no conflict resolution in v1

### 2. Settings Window

Tauri custom window (native, not a web dialog).

**Categories:**
| Section | Settings | Storage |
|---------|----------|---------|
| General | Data directory, language/locale, auto-start at login | Tauri store-plugin (JSON) |
| Editor | Default format (docx/odt/txt), autosave interval, spellcheck | Tauri store-plugin |
| Network | Proxy settings, server URL | Tauri store-plugin |
| Appearance | Theme (light/dark/system), font size, toolbar layout | Tauri store-plugin |

**Implementation:**
- Tauri command `open_settings()` → creates new native window
- Settings page is a web view loaded from embedded assets (not external URL)
- Changes take effect immediately (no restart required where possible)
- Cancel button reverts unsaved changes

### 3. Plugin System

Lightweight sandboxed JavaScript plugin system.

**Directory**: `~/.config/world-office/plugins/`
**Format**: Single `.js` file per plugin, exports hooks.
**API surface**:
```js
// Plugin API (injected globals)
worldOffice.toolbar.addButton({ id: 'my-plugin', label: 'My Action', icon, onClick })
worldOffice.editor.on('documentSaved', (doc) => { ... })
worldOffice.editor.getDocument()  // returns document model
worldOffice.ui.showToast(message)
```

**Lifecycle:**
1. Plugin directory scanned on app start
2. Each `.js` file loaded into QuickJS WASM sandbox (secure, no native access)
3. Plugin's `activate()` called with API object
4. File watcher detects new/enabled plugins for hot-reload
5. Enable/disable from Settings → Plugins panel

**V1 scope**: toolbar buttons + document event hooks. No npm dependencies, no network access.

### 4. Integration Tests

| Test | Setup | Verifies |
|------|-------|----------|
| App launches | `tauri-driver` → WebDriver | Window renders, toolbar visible |
| Create & save | WebDriver click type | File created on disk with content |
| Settings toggle | Open settings → change → close | Preference persists (JSON file) |
| Offline badge | Intercept network → `navigator.onLine=false` | Badge displays |
| Plugin load | Drop file in plugin dir | Button appears in toolbar |

**CI**: Run tests headless with `xvfb-run` on ubuntu-24.04.
**Tooling**: `@tauri-apps/testdriver` + Playwright/WebDriver.

## Error Handling

- **CI failure**: Build artifacts not published, previous release remains latest
- **Debian repo corruption**: Previous `Release` + `Packages` files preserved in git, manual revert possible
- **GPG key loss**: Rotate key, update all users (documented procedure)
- **Plugin crash**: Plugin sandboxed — crash does not affect main app
- **Offline data loss**: `localStorage` persisted on disk, survives restart

## Files to Create

| File | Purpose |
|------|---------|
| `.forgejo/workflows/desktop-release.yml` | CI workflow for build + publish |
| `desktop/tauri-poc/scripts/debian-repo.sh` | Package repository management script |
| `desktop/tauri-poc/scripts/gpg-init.sh` | GPG key setup script (one-time) |
| `desktop/tauri-poc/settings.html` | Settings window web view |
| `desktop/tauri-poc/src/settings.rs` | Tauri commands for settings CRUD |
| `desktop/tauri-poc/src/plugins.rs` | Plugin loader + sandbox |
| `docs/desktop/build-guide.md` | Developer build docs (macOS/Windows manual) |

## Versioning

- **Initial version**: `0.1.0` (matches current project phase; semver pre-release)
- **Nightlies**: Published to same Debian repo under `dists/nightly/` suite
- **Version bumps**: Manual tag `v0.1.0` → CI publishes to `dists/stable/`
  - Tag `v0.1.0-nightly.20260525` → CI publishes to `dists/nightly/`
