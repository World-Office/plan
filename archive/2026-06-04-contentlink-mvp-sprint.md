# Sprint: ContentLink MVP

**Date:** 2026-06-04
**Duration:** ~3-4 days
**Based on:** `2026-06-03-contentlink-implementation.md` (full plan)

## Scope (MVP)

Tasks 1-6 from the full plan, but Tasks 5 (frontend) is minimal:
- Store + hook + basic list panel + LeftMenu entry
- No resolve/navigate polish, no outbound links UI
- Full React panel deferred to follow-up

## Work Breakdown

| # | Task | Files | Depends On |
|---|------|-------|-----------|
| 1 | Database: content_links table + CRUD | `repository.rs` | — |
| 2 | API: 5 REST routes + tests | `lib.rs`, `integration_test.rs` | 1 |
| 3 | MCP Client: 3 methods | `client.rs` | 2 (API shape known) |
| 4 | MCP Tools: 3 tool defs + handlers | `tools.rs` | 3 |
| 5 | Frontend: minimal store/hook/panel + LeftMenu | `ContentLinkStore.ts`, `useContentLinks.ts`, `ContentLinkPanel.tsx`, `ContentLinkList.tsx`, `LeftMenu.tsx`, `App.tsx` | — (parallel) |
| 6 | Verification + ROADMAP | all | 1-5 |

## Track B (parallel)

| # | Task | Notes |
|---|------|-------|
| B1 | Fix conversion-service tests (3 failures) | From previous sprint |
| B2 | Update ROADMAP.md | MCP Server + ContentLink |
| B3 | Fix flaky collaboration-client tests (if time) | 2 async timing tests |

## Execution Plan

Phase 1: Tasks 1-2 (DB + API) — sequential, must build on each other
Phase 2: Tasks 3-5 (MCP + Frontend) — parallel, independent
Phase 3: Task 6 (verification)
Track B: throughout
