# Sprint: Legacy Editor Removal

**Date:** 2026-06-01
**Source Plan:** server/.sisyphus/plans/legacy-editor-removal.md

## Overview

Remove 5 legacy vanilla JavaScript editors (~22,000 files) while preserving modern React equivalents and third-party embed integration API.

## Deliverables

- [x] Legacy documenteditor deleted (`apps/web/apps/documenteditor/`)
- [x] Legacy spreadsheeteditor deleted (`apps/web/apps/spreadsheeteditor/`)
- [x] Legacy presentationeditor deleted (`apps/web/apps/presentationeditor/`)
- [x] Legacy pdfeditor + visioeditor deleted (`apps/web/apps/pdfeditor/`, `apps/web/apps/visioeditor/`)
- [x] Documentation updated to reflect React-only architecture
- [x] Final verification — builds, tests, no orphan references

## Results

- **5,981 files deleted** across 5 legacy editors
- **516,755 lines removed** (source: help resources, images, JS, LESS)
- **Documentation updated:** `apps/web/AGENTS.md`, `apps/web/Readme.md`
- **Verification:** All React editors build ✓, typecheck passes ✓, zero orphan references ✓
- **Git diff:** +14 / -62 lines in documentation
- **Commit:** `docs(web): update documentation to reflect React-only architecture`
- **Preserved:** `api/documents/`, `common/`, `vendor/`, `theme/`, `translation/`

## Guardrails

- DO NOT delete `api/documents/` — embed API used by all third-party integrations
- DO NOT delete `apps/web/apps/common/` — shared legacy code for embed API
- DO NOT delete `apps/web/vendor/` — vendored libs for embed API
- DO NOT delete `apps/web/theme/` or `apps/web/translation/` — used by embed API
- DO NOT delete `apps/web/packages/` — shared packages for React editors
- DO NOT modify any React editor code (`*-react/` directories or `editor-shell/`)
- DO NOT modify any `packages/` code, Rust backend, or `integrations/`
- Each deletion is independently committed and reviewable

## Execution

Tasks execute sequentially with build verification after each:

1. Delete legacy documenteditor (~5,033 files)
2. Delete legacy spreadsheeteditor (~12,528 files)
3. Delete legacy presentationeditor (~4,477 files)
4. Delete legacy pdfeditor + visioeditor (smallest)
5. Update documentation (AGENTS.md, README.md, etc.)
6. Final verification (cargo test, pnpm build/typecheck/lint)
