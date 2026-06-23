# Sprint: Legacy Editor Removal

**Date:** 2026-06-01
**Status:** Complete
**Source Plan:** `server/.sisyphus/plans/legacy-editor-removal.md` (detailed task breakdown, 1188 lines)

## Objective

Delete 5 legacy vanilla JavaScript editors (~22,000 files) from `apps/web/apps/` while preserving modern React equivalents (`*-react/`). This completes Phase 4 (Web UI migration), which was marked "complete" in ROADMAP.md but still had legacy code in the tree.

## What's Being Deleted

| Editor | Directory | Est. Files | React Equivalent (SAFE) |
|--------|-----------|------------|-------------------------|
| Document Editor | `apps/web/apps/documenteditor/` | ~5,033 | `apps/web/apps/documenteditor-react/` |
| Spreadsheet Editor | `apps/web/apps/spreadsheeteditor/` | ~12,528 | `apps/web/apps/spreadsheeteditor-react/` |
| Presentation Editor | `apps/web/apps/presentationeditor/` | ~4,477 | `apps/web/apps/presentationeditor-react/` |
| PDF Editor | `apps/web/apps/pdfeditor/` | small | `apps/web/apps/pdfeditor-react/` |
| Visio Editor | `apps/web/apps/visioeditor/` | small | `apps/web/apps/visioeditor-react/` |

## What MUST NOT Be Deleted (Guardrails)

- **DO NOT** delete `apps/web/apps/api/documents/` — embed API used by all third-party integrations (Nextcloud, OpenCloud, etc.)
- **DO NOT** delete `apps/web/apps/common/` — shared legacy code used by embed API
- **DO NOT** delete `apps/web/vendor/` — vendored libs used by embed API
- **DO NOT** delete `apps/web/theme/` or `apps/web/translation/` — legacy themes/translations used by embed API
- **DO NOT** modify any React editor code (`*-react/` or `editor-shell/`)
- **DO NOT** modify any `packages/`, Rust backend, or `integrations/` code

## Tasks (Sequential)

### Task 1: Delete Legacy Document Editor
- Delete `apps/web/apps/documenteditor/` entirely
- Verify: `ls apps/web/apps/documenteditor/` → "No such file or directory"
- Build verify: `pnpm install --frozen-lockfile && pnpm typecheck && pnpm build`
- Orphan check: grep React editors for legacy documenteditor/ paths
- Commit: `refactor(web): remove legacy documenteditor (vanilla JS)`

### Task 2: Delete Legacy Spreadsheet Editor
- Delete `apps/web/apps/spreadsheeteditor/` entirely
- Same verification pattern as Task 1
- Commit: `refactor(web): remove legacy spreadsheeteditor (vanilla JS)`

### Task 3: Delete Legacy Presentation Editor
- Delete `apps/web/apps/presentationeditor/` entirely
- Same verification pattern as Task 1
- Commit: `refactor(web): remove legacy presentationeditor (vanilla JS)`

### Task 4: Delete Legacy PDF Editor + Visio Editor
- Delete `apps/web/apps/pdfeditor/` and `apps/web/apps/visioeditor/`
- Combined task (smallest editors)
- Commit: `refactor(web): remove legacy pdfeditor and visioeditor (vanilla JS)`

### Task 5: Update Documentation
- Update: AGENTS.md, README.md, apps/web/AGENTS.md, apps/web/Readme.md, ROADMAP.md
- Remove all references to legacy editor directories (non-React paths)
- Update file counts (~22K fewer files)
- Mark Phase 4 as truly complete
- Commit: `docs: update documentation to reflect React-only architecture`

### Task 6: Final Verification
- Clean install: `rm -rf node_modules .pnpm-store && pnpm install --frozen-lockfile`
- Full typecheck/build/lint
- Verify all 5 legacy directories gone
- Verify all 5 React editors build independently
- Verify no orphan references
- Verify Rust backend unaffected: `cargo test -p wo-docserver --lib`
- All evidence saved to `.sisyphus/evidence/`

## Verification Commands

```bash
# All 5 legacy directories deleted
ls apps/web/apps/documenteditor/ 2>&1 | grep "No such file"
ls apps/web/apps/spreadsheeteditor/ 2>&1 | grep "No such file"
ls apps/web/apps/presentationeditor/ 2>&1 | grep "No such file"
ls apps/web/apps/pdfeditor/ 2>&1 | grep "No such file"
ls apps/web/apps/visioeditor/ 2>&1 | grep "No such file"

# Workspace builds
pnpm typecheck
pnpm build
pnpm lint

# No orphan references
grep -r "documenteditor/\|spreadsheeteditor/\|presentationeditor/" apps/web/apps/*-react/ | wc -l
# Expected: 0

# Rust backend unaffected
cargo test -p wo-docserver --lib

# React editors still build
for d in documenteditor spreadsheeteditor presentationeditor pdfeditor visioeditor; do
  cd apps/web/apps/${d}-react && pnpm build 2>&1 | tail -3
done
```

## Success Criteria

- [x] All 5 legacy editor directories deleted (verified by ls)
- [x] All 5 React editors build successfully
- [x] pnpm typecheck passes
- [x] Zero orphan references to legacy paths in React editors
- [x] Documentation updated to reflect React-only architecture
- [x] Embed API (`api/documents/`), shared legacy infra (`common/`, `vendor/`, `theme/`, `translation/`) preserved
- [~] pnpm lint — pre-existing issue in `packages/collaboration-client` (unrelated)
- [~] Rust backend tests — pre-existing setup issue (no Docker/runtime)

## Note on Shared Legacy Infrastructure

The `api/documents/`, `common/`, `vendor/`, `theme/`, and `translation/` directories are deliberately **NOT** being deleted in this sprint — they form a cohesive legacy embed system used by all third-party integrations (Nextcloud, OpenCloud, etc.). Deleting these would be a breaking change requiring a separate coordination effort with integration maintainers. The existing plan includes a standalone task for this that is currently deferred.
