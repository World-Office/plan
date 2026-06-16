# Sprint: Comments with @agent Mentions

**Date:** 2026-06-02
**Status:** Completed (6/6 tasks).
**Commits:** `18ad413d1`, `e18552533`, `a86beb33a`, `782258599`, `bdbbf4b8b`, `f032eb87e`
**Branches:** Pushed to both Codeberg (origin) and GitHub (tobias-weiss-ai-xr)

## Completed

### 1. Storage — comments table + REST CRUD ✓
- `services/storage-service/src/repository.rs`: `StoredComment` struct, `comments` table, CRUD methods (`insert_comment`, `list_comments`, `resolve_comment`, `delete_comment`, `list_mentions`)
- `services/storage-service/src/lib.rs`: REST endpoints at `/documents/{id}/comments/*` and `/mentions/{agent_name}`
- 6 new unit tests pass (`cargo test -p storage-service --lib`)
- Mention detection: `@agent_name` patterns extracted from comment text into JSON array

### 2. WebSocket CommentEvent Protocol ✓
- `services/coauthoring-service/src/main.rs`: `CommentEventData` struct, `WsMessage::CommentEvent` variant, broadcast via edit channel
- `packages/collaboration-client/src/protocol.ts`: `CommentEventData` interface, `comment_event` in `WsMessage`/`ServerMessage` unions, `parseServerMessage` handler

### 3. Client Wiring through useCollaboration ✓
- `packages/collaboration-client/src/client.ts`: `commentEvent` event, `sendCommentEvent` method, `handleMessage` routing (skip own echo)
- `packages/collaboration-react/src/hooks/useCollaboration.ts`: `onCommentEvent` callback, auto-routes to `CollaborationStore.addComment/addReply/resolveComment`, exports `sendCommentEvent`

### 4. React UI Components ✓
- `packages/collaboration-react/src/components/CommentInput.tsx`: Textarea with @mention autocomplete dropdown, Enter to submit
- `packages/collaboration-react/src/components/CommentThread.tsx`: Threaded comment display with resolve/reply actions, @mention highlighting, relative timestamps
- `packages/collaboration-react/src/components/CommentPanel.tsx`: Sidebar panel with Active/Resolved tabs, comment count badge, new comment input at bottom
- All exported from `index.ts`; 20/20 `pnpm typecheck` tasks pass

### 5. MCP Comment Tools ✓
- `services/mcp-server/src/client.rs`: Added `list_comments`, `add_comment`, `add_reply`, `resolve_comment`, `list_mentions` HTTP methods to `StorageClient`
- `services/mcp-server/src/tools.rs`: Added 4 MCP tools (`list_comments`, `add_comment`, `resolve_comment`, `list_mentions`) with tool definitions and handlers
- Agents can now discover their @mentions via `list_mentions`, read document comments, post comments, and resolve threads — all through the stdio MCP protocol
- `cargo check -p mcp-server` passes (using workspace nightly toolchain)

### 6. Integration + E2E Verification ✓
- `tests/tests/setup.js`: Added `storageServiceUrl` to config
- `tests/tests/e2e/api/comments.test.js`: 11 E2E tests covering full comment lifecycle:
  1. Create document (test fixture)
  2. Create comment with @agent mention (auto-extraction verified)
  3. Create comment with no mention
  4. List comments with threading
  5. Reply to a comment
  6. Reply appears nested under parent
  7. Resolve a comment
  8. Replies survive resolution
  9. List mentions for agent
  10. Empty mentions return empty array
  11. Error handling (missing fields, 404)
- All 21 storage-service unit tests pass, all TS typechecks pass, mcp-server compiles

## Objective

```
User writes comment → React CommentPanel
    ↓
collaboration-client (WebSocket) → CommentEvent message
    ↓
coauthoring-service (broadcast + persist to storage-service)
    ↓
storage-service SQLite (comments table)
    ↓
MCP server (list_mentions tool) ← Agents poll for @mentions
```

## Existing Infrastructure

- `CollaborationStore` in `packages/editor-stores` — already has `CollabComment` type with `id`, `userId`, `userName`, `text`, `timestamp`, `resolved`, `replies` (threaded!)
- Methods already exist: `addComment`, `resolveComment`, `addReply`, `setComments`, `setCommentMode`
- `comment: boolean` permission in `EditorPermissions`
- WebSocket protocol in `collaboration-client/src/protocol.ts` — needs comment event types added
- Rust coauthoring-service with WsMessage enum + presence broadcast — needs comment event handling
- storage-service SQLite with repository pattern — needs comments table

## Tasks

### Task 1: Comments table + Repository Methods (storage-service)

**Files:**
- Modify: `services/storage-service/src/repository.rs`
- Modify: `services/storage-service/src/lib.rs`

**Steps:**
- [ ] Add `StoredComment` struct to repository.rs
- [ ] Add `comments` table to `init_table()` (document_id, parent_id for threading, author_id, author_name, text, resolved, mentions JSON, created_at)
- [ ] Add methods: `insert_comment`, `list_comments(document_id)`, `resolve_comment`, `delete_comment`
- [ ] Add snapshot REST endpoints to lib.rs:
  - `GET /documents/{id}/comments` — list comments
  - `POST /documents/{id}/comments` — create comment
  - `POST /comments/{id}/resolve` — resolve a comment
  - `DELETE /comments/{id}` — delete a comment
  - `POST /comments/{id}/replies` — add reply
- [ ] Add tests for comment CRUD
- [ ] Commit: `feat(storage): add comments table, repository, and REST endpoints`

### Task 2: CommentEvent WebSocket Protocol (Rust + TypeScript)

**Files:**
- Modify: `services/coauthoring-service/src/main.rs`
- Modify: `packages/collaboration-client/src/protocol.ts`

**Steps:**
- [ ] Add `CommentEvent` enum to Rust server (variants: `added`, `resolved`, `deleted`, `reply_added`)
- [ ] Add `CommentData` struct matching the storage-service comment model
- [ ] Add `comment` variant to Rust `WsMessage` enum
- [ ] Add comment broadcast channel (like existing `presence_tx`) in coauthoring-service
- [ ] Handle incoming comment events: broadcast to all session participants
- [ ] Add matching types to TypeScript protocol.ts: `CommentEvent`, `CommentData`
- [ ] Add `comment` variant to `WsMessage` and `ServerMessage` discriminated unions
- [ ] Update `parseServerMessage` to handle comment events
- [ ] Add `createCommentUpdate` helper function
- [ ] Update client.ts handleMessage to route comment events to `collaborationClient.onComment` callback
- [ ] Verify TypeScript compiles: `pnpm typecheck`
- [ ] Verify Rust compiles: `cargo check -p coauthoring-service`
- [ ] Commit: `feat(collaboration): add CommentEvent WebSocket protocol`

### Task 3: Wire Comment Events into CollaborationStore

**Files:**
- Modify: `packages/collaboration-client/src/index.ts` (add `onComment` event to client interface)
- Modify: `packages/collaboration-react/src/hooks/useCollaboration.ts`
- Modify: `packages/editor-stores/src/stores/CollaborationStore.ts`

**Steps:**
- [ ] Add `CommentEvent` type to collaboration-client/index.ts export
- [ ] Add comment event handling to the WebSocket message dispatch
- [ ] Wire `useCollaboration` hook to call store methods on comment events
- [ ] Verify TypeScript compiles
- [ ] Commit: `feat(collaboration): wire comment events into CollaborationStore`

### Task 4: Comment React UI Components

**Files:**
- Create: `packages/collaboration-react/src/components/CommentPanel.tsx`
- Create: `packages/collaboration-react/src/components/CommentThread.tsx`
- Create: `packages/collaboration-react/src/components/CommentInput.tsx`
- Create: `packages/collaboration-react/src/components/CommentMentionAutocomplete.tsx`
- Modify: `packages/collaboration-react/src/index.ts`

**Steps:**
- [ ] Create `CommentPanel` — sidebar panel showing list of comment threads for the current document
- [ ] Create `CommentThread` — renders a comment + its reply chain
- [ ] Create `CommentInput` — textarea with @mention autocomplete (parses `@username` patterns)
- [ ] Create `CommentMentionAutocomplete` — dropdown showing matching agent/user names on `@` input
- [ ] Wire comment creation to REST API (`POST /documents/{id}/comments`)
- [ ] Wire resolve/delete buttons
- [ ] Handle @agent mentions: store mention metadata in comment (parse `@agent_name` from text)
- [ ] Add toggle button in editor toolbar (isCommentMode)
- [ ] Export all components from `packages/collaboration-react/src/index.ts`
- [ ] Verify TypeScript compiles: `pnpm typecheck`
- [ ] Commit: `feat(collaboration-react): add CommentPanel, CommentThread, CommentInput with @mention autocomplete`

### Task 5: @agent Mention Detection + MCP Tools

**Files:**
- Modify: `services/mcp-server/src/tools.rs`
- Create: `services/mcp-server/src/comments.rs`

**Steps:**
- [ ] Add comments client module (HTTP client to storage-service comment endpoints)
- [ ] Add MCP tool: `list_mentions` — returns comments where `@agent_name` or `@all` is mentioned
  - Takes: `agent_name` (optional, default: current agent), `document_id` (optional filter)
  - Returns: list of comments with context (document, author, text, thread)
- [ ] Add MCP tool: `reply_to_comment` — allows agent to reply to a comment thread
  - Takes: `comment_id`, `text`
- [ ] Add MCP tool: `resolve_comment` — mark a comment/resolution as resolved
  - Takes: `comment_id`
- [ ] Register new tools in main.rs tool list
- [ ] Verify Rust compiles: `cargo check -p wo-mcp-server`
- [ ] Commit: `feat(mcp-server): add comment mention tools for agent collaboration`

### Task 6: Integration + E2E Verification

**Files:**
- Modify: Various (testing/tweaking only)
- Create: `packages/collaboration-react/__tests__/CommentPanel.test.tsx`

**Steps:**
- [ ] Add unit tests for CommentPanel components (render, add comment, resolve, @mention)
- [ ] Add unit tests for storage-service comment repository methods
- [ ] Verify full stack: `pnpm typecheck && pnpm build --filter=@world-office/collaboration-react`
- [ ] Verify Rust: `cargo test -p storage-service`
- [ ] Verify Rust: `cargo check --workspace` (excluding wo-pdf, wo-webdav)
- [ ] Commit: `test: add comment system tests + final verification`

## Guardrails

- DO NOT modify existing document editing functionality
- DO NOT modify the CRDT or edit operation pipeline
- DO NOT remove or rename existing CollaborationStore methods
- Comments data model must be backward-compatible with existing CollabComment interface

## Success Criteria

- [ ] Comments persist to SQLite and survive service restart
- [ ] Comment events sync via WebSocket in real-time
- [ ] Comment threads (parent + replies) display correctly in React components
- [ ] @mentions are parsed from comment text and stored as metadata
- [ ] MCP `list_mentions` tool returns agent-relevant comments
- [ ] MCP `reply_to_comment` tool lets agents participate in threads
- [ ] TypeScript typecheck passes
- [ ] Rust workspace compiles
- [ ] Existing collaboration functionality unaffected
