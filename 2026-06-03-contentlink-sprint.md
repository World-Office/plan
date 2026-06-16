# Sprint: Cross-document ContentLink

**Date:** 2026-06-03
**Duration:** ~1 week
**Status:** Planned

## Objective

Implement cross-document live references (ContentLink) — the Tier 2 ROADMAP item. Users can embed a live reference to content in another document, which stays in sync as the source document changes. Also study AOSE's existing ContentLink implementation to inform our design.

## Background

- Comments with @agent mentions — ✅ done (2026-06-02)
- MCP Server + Version Snapshots — ✅ done (previously)
- ContentLink is the next Tier 2 item per ROADMAP.md
- [AgentOfficeSuite](https://github.com/manpoai/AgentOfficeSuite) has a working ContentLink implementation (Apache 2.0) — worth studying

## Work Breakdown

### Track A: ContentLink Design & Implementation (Primary)

| # | Task | Status | Notes |
|---|------|--------|-------|
| A1 | **Study AOSE ContentLink approach** | Pending | Fetch AOSE docs/source for ContentLink patterns — wire format, rendering, update protocol |
| A2 | **Design ContentLink data model** | Pending | Reference type, source doc/section pointer, display text, allowed content types |
| A3 | **Design ContentLink update protocol** | Pending | How do references update when source changes? Polling vs push vs lazy resolution |
| A4 | **Implement server-side ContentLink storage** | Pending | New table(s) in storage-service, CRUD API |
| A5 | **Implement ContentLink resolution** | Pending | Server resolves ContentLinks to current source content on read |
| A6 | **Implement ContentLink in editor** | Pending | React component for inserting/displaying ContentLinks, inline block type |
| A7 | **Implement auto-update on source change** | Pending | When source doc content changes, update references in target docs |
| A8 | **Add MCP tools for ContentLink** | Pending | Agent tools: create_contentlink, resolve_contentlink, list_contentlinks |
| A9 | **E2E tests** | Pending | Playwright tests covering ContentLink lifecycle |
| A10 | **Update ROADMAP.md** | Pending | Mark MCP Server + Version Snapshots done, ContentLink in progress |

### Track B: Quick Cleanup (Parallel)

| # | Task | Status | Notes |
|---|------|--------|-------|
| B1 | **Fix conversion-service tests** (3 failures) | Pending | Assertion errors: error message format, format count mismatch, output data structure |
| B2 | **Fix flaky collaboration-client tests** | Pending | 2 async timing-dependent tests |
| B3 | **Update ROADMAP.md** (MCP Server done) | Pending | Housekeeping |

### Track C: Desktop Distribution Pipeline (If Time Permits)

| # | Task | Status | Notes |
|---|------|--------|-------|
| C1 | **Review existing design doc** | Pending | `/home/weiss/git/World-Office/plan/2026-05-24-tauri-desktop-distribution-features-design.md` |
| C2 | **Implement Debian repo infra** | Pending | Codeberg Pages hosting, GPG signing |
| C3 | **Implement CI workflow** | Pending | Forgejo Actions workflow for repo updates |

## AgentOfficeSuite ContentLink — Initial Notes

From AOSE README analysis (2026-06-03):

- AOSE Docs editor includes "cross-document live references (ContentLink)" as a content block type alongside paragraph, heading, table, image, Mermaid, etc.
- ContentLink is one of 19 content blocks in their rich-text editor
- Agents create/edit ContentLinks through MCP tools (same pattern as our approach)
- AOSE is Apache 2.0 licensed — study their implementation patterns
- AOSE is a local-first service (`npx aose-main`), different architecture from our server-based approach

## Verification

- [ ] All Rust: `cargo check --workspace` — 0 errors
- [ ] Lint: `cargo clippy --workspace` — 0 new warnings
- [ ] Format: `cargo fmt --all`
- [ ] Tests: `cargo test --workspace --lib -- --test-threads=1` — all pass
- [ ] TypeScript: `pnpm lint && pnpm typecheck`
- [ ] E2E: ContentLink lifecycle tests pass
- [ ] ROADMAP.md updated
