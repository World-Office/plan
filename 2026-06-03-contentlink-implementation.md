# Cross-document ContentLink Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: subagent-driven-development or executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement cross-document live references (ContentLink) — embed content from one document into another, resolving and displaying the source document's content inline on every read.

**Architecture:** ContentLinks are stored as a separate database resource (like comments) not embedded in OOXML. Storage-service provides REST CRUD + resolution endpoint. MCP server exposes agent tools. The React editor displays ContentLinks in a dedicated panel where users can see all inbound/outbound references, navigate to source documents, and preview resolved content. Resolution is lazy-on-read: the content is fetched from the source document each time the target is opened.

**Tech Stack:** Rust (storage-service + MCP server, axum + rusqlite), React/TypeScript (documenteditor-react), SQLite (storage)

**V1 Scope:** Database + API + MCP tools. Editor UI is a dedicated panel (like the comment panel), not inline document embedding. Cross-document references via sidebar with source preview and navigation.

---

## File Structure

### New files:
- `services/storage-service/src/migrations/003_content_links.sql` — SQL migration
- `services/storage-service/` — modify `repository.rs` (add content_link queries), `lib.rs` (add API routes), `main.rs` (no changes needed)
- `services/mcp-server/` — modify `tools.rs` (add 3 tools), `client.rs` (add StorageClient methods)
- `apps/web/apps/documenteditor-react/src/components/ContentLinkPanel.tsx` — React component
- `apps/web/apps/documenteditor-react/src/components/ContentLinkList.tsx` — list sub-component
- `apps/web/apps/documenteditor-react/src/hooks/useContentLinks.ts` — API hook
- `apps/web/apps/documenteditor-react/src/stores/ContentLinkStore.ts` — MobX store

### Modified files:
- `services/storage-service/src/repository.rs` — add content_links table init, CRUD methods
- `services/storage-service/src/lib.rs` — add 5 new API routes
- `services/storage-service/tests/integration_test.rs` — add ContentLink API tests
- `services/mcp-server/src/client.rs` — add 3 StorageClient methods
- `services/mcp-server/src/tools.rs` — add 3 tool definitions + handlers
- `services/mcp-server/src/tools.rs` — update `instructions` string
- `apps/web/apps/documenteditor-react/src/App.tsx` — add ContentLink panel route
- `apps/web/apps/documenteditor-react/src/components/LeftMenu/LeftMenu.tsx` — add ContentLink button

---

### Task 1: Database — content_links table + CRUD repository methods

**Files:**
- Modify: `services/storage-service/src/repository.rs`

- [ ] **Step 1: Add `ContentLink` struct and `init_table` migration**

Add after the `StoredComment` struct:

```rust
#[derive(Debug, Clone)]
pub struct ContentLink {
    pub id: String,
    pub source_document_id: String,
    pub source_document_name: String,
    pub target_document_id: String,
    pub target_document_name: String,
    pub display_text: String,
    pub resolved_content: String,
    pub resolved_at: Option<String>,
    pub created_at: String,
}
```

In `init_table()`, add after the comments table creation:

```rust
CREATE TABLE IF NOT EXISTS content_links (
    id                  TEXT PRIMARY KEY,
    source_document_id  TEXT NOT NULL REFERENCES files(id) ON DELETE CASCADE,
    source_document_name TEXT NOT NULL,
    target_document_id  TEXT NOT NULL REFERENCES files(id) ON DELETE CASCADE,
    target_document_name TEXT NOT NULL,
    display_text        TEXT NOT NULL DEFAULT '',
    resolved_content    TEXT NOT NULL DEFAULT '',
    resolved_at         TEXT,
    created_at          TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_content_links_source ON content_links(source_document_id);
CREATE INDEX IF NOT EXISTS idx_content_links_target ON content_links(target_document_id);
```

- [ ] **Step 2: Add `insert_content_link` method**

```rust
pub fn insert_content_link(
    &mut self,
    source_document_id: &str,
    source_document_name: &str,
    target_document_id: &str,
    target_document_name: &str,
    display_text: &str,
) -> Result<String, rusqlite::Error> {
    let id = uuid::Uuid::new_v4().to_string();
    let created_at = chrono::Utc::now().to_rfc3339();
    self.conn.execute(
        "INSERT INTO content_links (id, source_document_id, source_document_name, target_document_id, target_document_name, display_text, resolved_content, resolved_at, created_at)
         VALUES (?1, ?2, ?3, ?4, ?5, ?6, '', NULL, ?7)",
        rusqlite::params![id, source_document_id, source_document_name, target_document_id, target_document_name, display_text, created_at],
    )?;
    Ok(id)
}
```

- [ ] **Step 3: Add `get_content_link`, `list_content_links_by_target`, `list_content_links_by_source`, `delete_content_link`, `update_resolved_content` methods**

```rust
pub fn get_content_link(&self, id: &str) -> Result<Option<ContentLink>, rusqlite::Error> {
    let mut stmt = self.conn.prepare(
        "SELECT id, source_document_id, source_document_name, target_document_id, target_document_name, display_text, resolved_content, resolved_at, created_at
         FROM content_links WHERE id = ?1",
    )?;
    let mut rows = stmt.query(rusqlite::params![id])?;
    match rows.next()? {
        Some(row) => Ok(Some(row_to_content_link(row)?)),
        None => Ok(None),
    }
}

pub fn list_content_links_by_target(&self, document_id: &str) -> Result<Vec<ContentLink>, rusqlite::Error> {
    let mut stmt = self.conn.prepare(
        "SELECT id, source_document_id, source_document_name, target_document_id, target_document_name, display_text, resolved_content, resolved_at, created_at
         FROM content_links WHERE target_document_id = ?1 ORDER BY created_at DESC",
    )?;
    let rows = stmt.query_map(rusqlite::params![document_id], row_to_content_link)?;
    rows.collect::<Result<Vec<_>, _>>()
}

pub fn list_content_links_by_source(&self, document_id: &str) -> Result<Vec<ContentLink>, rusqlite::Error> {
    let mut stmt = self.conn.prepare(
        "SELECT id, source_document_id, source_document_name, target_document_id, target_document_name, display_text, resolved_content, resolved_at, created_at
         FROM content_links WHERE source_document_id = ?1 ORDER BY created_at DESC",
    )?;
    let rows = stmt.query_map(rusqlite::params![document_id], row_to_content_link)?;
    rows.collect::<Result<Vec<_>, _>>()
}

pub fn delete_content_link(&mut self, id: &str) -> Result<bool, rusqlite::Error> {
    let affected = self.conn.execute(
        "DELETE FROM content_links WHERE id = ?1",
        rusqlite::params![id],
    )?;
    Ok(affected > 0)
}

pub fn update_resolved_content(&mut self, id: &str, content: &str) -> Result<bool, rusqlite::Error> {
    let now = chrono::Utc::now().to_rfc3339();
    let affected = self.conn.execute(
        "UPDATE content_links SET resolved_content = ?1, resolved_at = ?2 WHERE id = ?3",
        rusqlite::params![content, now, id],
    )?;
    Ok(affected > 0)
}
```

- [ ] **Step 4: Add `row_to_content_link` helper**

```rust
fn row_to_content_link(row: &rusqlite::Row<'_>) -> Result<ContentLink, rusqlite::Error> {
    Ok(ContentLink {
        id: row.get(0)?,
        source_document_id: row.get(1)?,
        source_document_name: row.get(2)?,
        target_document_id: row.get(3)?,
        target_document_name: row.get(4)?,
        display_text: row.get(5)?,
        resolved_content: row.get(6)?,
        resolved_at: row.get(7)?,
        created_at: row.get(8)?,
    })
}
```

- [ ] **Step 5: Run tests**

Run: `cargo test -p storage-service --lib`
Expected: all existing tests pass, no new tests yet

- [ ] **Step 6: Commit**

```bash
git add services/storage-service/src/repository.rs
git commit -m "feat(storage): add content_links table and CRUD repository methods"
```

---

### Task 2: Storage service — ContentLink REST API routes

**Files:**
- Modify: `services/storage-service/src/lib.rs`
- Modify: `services/storage-service/tests/integration_test.rs`

- [ ] **Step 1: Define request/response types**

Add to `lib.rs` after `CreateCommentRequest`:

```rust
#[derive(Debug, Deserialize)]
pub struct CreateContentLinkRequest {
    pub source_document_id: String,
    pub source_document_name: String,
    pub target_document_name: String,
    pub display_text: Option<String>,
}

#[derive(Debug, Serialize)]
pub struct ContentLinkResponse {
    pub id: String,
    pub source_document_id: String,
    pub source_document_name: String,
    pub target_document_id: String,
    pub target_document_name: String,
    pub display_text: String,
    pub resolved_content: String,
    pub resolved_at: Option<String>,
    pub created_at: String,
}

#[derive(Debug, Serialize)]
pub struct ContentLinkListResponse {
    pub content_links: Vec<ContentLinkResponse>,
    pub count: usize,
}
```

- [ ] **Step 2: Add 5 handler functions**

Add after `list_mentions`:

```rust
pub async fn create_content_link(
    State(state): State<Arc<AppState>>,
    Path(target_document_id): Path<String>,
    Json(payload): Json<CreateContentLinkRequest>,
) -> Result<(StatusCode, Json<ContentLinkResponse>), (StatusCode, Json<ErrorResponse>)> {
    // Verify source document exists
    let source_name = {
        let repo = state.repo.lock().await;
        match repo.get(&payload.source_document_id) {
            Ok(Some(file)) => file.name,
            Ok(None) => {
                return Err((StatusCode::NOT_FOUND, Json(ErrorResponse {
                    error: format!("Source document {} not found", payload.source_document_id),
                    code: 404,
                })));
            }
            Err(e) => return Err((StatusCode::INTERNAL_SERVER_ERROR, Json(ErrorResponse {
                error: format!("Failed to verify source: {}", e), code: 500,
            }))),
        }
    };

    let display_text = payload.display_text.unwrap_or_else(|| source_name.clone());
    let mut repo = state.repo.lock().await;

    match repo.insert_content_link(
        &payload.source_document_id,
        &payload.source_document_name,
        &target_document_id,
        &payload.target_document_name,
        &display_text,
    ) {
        Ok(id) => {
            let created_at = chrono::Utc::now().to_rfc3339();
            tracing::info!(content_link_id = %id, target = %target_document_id, source = %payload.source_document_id, "content link created");
            Ok((StatusCode::CREATED, Json(ContentLinkResponse {
                id, source_document_id: payload.source_document_id,
                source_document_name: payload.source_document_name,
                target_document_id, target_document_name: payload.target_document_name,
                display_text, resolved_content: String::new(),
                resolved_at: None, created_at,
            })))
        }
        Err(e) => Err((StatusCode::INTERNAL_SERVER_ERROR, Json(ErrorResponse {
            error: format!("Failed to create content link: {}", e), code: 500,
        }))),
    }
}

pub async fn list_content_links(
    State(state): State<Arc<AppState>>,
    Path(document_id): Path<String>,
) -> Result<Json<ContentLinkListResponse>, (StatusCode, Json<ErrorResponse>)> {
    let repo = state.repo.lock().await;
    let links = repo.list_content_links_by_target(&document_id).map_err(|e| {
        (StatusCode::INTERNAL_SERVER_ERROR, Json(ErrorResponse {
            error: format!("Failed to list content links: {}", e), code: 500,
        }))
    })?;
    let responses: Vec<ContentLinkResponse> = links.into_iter().map(|l| ContentLinkResponse {
        id: l.id, source_document_id: l.source_document_id,
        source_document_name: l.source_document_name,
        target_document_id: l.target_document_id,
        target_document_name: l.target_document_name,
        display_text: l.display_text, resolved_content: l.resolved_content,
        resolved_at: l.resolved_at, created_at: l.created_at,
    }).collect();
    let count = responses.len();
    Ok(Json(ContentLinkListResponse { content_links: responses, count }))
}

pub async fn resolve_content_link(
    State(state): State<Arc<AppState>>,
    Path(link_id): Path<String>,
) -> Result<Json<ContentLinkResponse>, (StatusCode, Json<ErrorResponse>)> {
    let link = {
        let repo = state.repo.lock().await;
        match repo.get_content_link(&link_id) {
            Ok(Some(l)) => l,
            Ok(None) => return Err((StatusCode::NOT_FOUND, Json(ErrorResponse {
                error: format!("Content link {} not found", link_id), code: 404,
            }))),
            Err(e) => return Err((StatusCode::INTERNAL_SERVER_ERROR, Json(ErrorResponse {
                error: format!("Failed to get content link: {}", e), code: 500,
            }))),
        }
    };

    // Read source document content from disk
    let (content, content_type) = {
        let repo = state.repo.lock().await;
        match repo.get(&link.source_document_id) {
            Ok(Some(file)) => {
                let data = tokio::fs::read_to_string(&file.storage_path).await
                    .map_err(|e| (StatusCode::INTERNAL_SERVER_ERROR, Json(ErrorResponse {
                        error: format!("Failed to read source document: {}", e), code: 500,
                    })))?;
                (data, file.content_type.clone())
            }
            Ok(None) => return Err((StatusCode::NOT_FOUND, Json(ErrorResponse {
                error: format!("Source document {} not found", link.source_document_id), code: 404,
            }))),
            Err(e) => return Err((StatusCode::INTERNAL_SERVER_ERROR, Json(ErrorResponse {
                error: format!("Failed to get source: {}", e), code: 500,
            }))),
        }
    };

    // Truncate content to first N characters for preview
    let preview = if content.len() > 500 {
        format!("{}...", &content[..500])
    } else {
        content.clone()
    };

    let mut repo = state.repo.lock().await;
    repo.update_resolved_content(&link_id, &preview).map_err(|e| {
        (StatusCode::INTERNAL_SERVER_ERROR, Json(ErrorResponse {
            error: format!("Failed to update resolved content: {}", e), code: 500,
        }))
    })?;

    let resolved_at = Some(chrono::Utc::now().to_rfc3339());
    Ok(Json(ContentLinkResponse {
        id: link.id, source_document_id: link.source_document_id,
        source_document_name: link.source_document_name,
        target_document_id: link.target_document_id,
        target_document_name: link.target_document_name,
        display_text: link.display_text, resolved_content: preview,
        resolved_at, created_at: link.created_at,
    }))
}

pub async fn list_outbound_content_links(
    State(state): State<Arc<AppState>>,
    Path(document_id): Path<String>,
) -> Result<Json<ContentLinkListResponse>, (StatusCode, Json<ErrorResponse>)> {
    let repo = state.repo.lock().await;
    let links = repo.list_content_links_by_source(&document_id).map_err(|e| {
        (StatusCode::INTERNAL_SERVER_ERROR, Json(ErrorResponse {
            error: format!("Failed to list outbound links: {}", e), code: 500,
        }))
    })?;
    let responses: Vec<ContentLinkResponse> = links.into_iter().map(|l| ContentLinkResponse {
        id: l.id, source_document_id: l.source_document_id,
        source_document_name: l.source_document_name,
        target_document_id: l.target_document_id,
        target_document_name: l.target_document_name,
        display_text: l.display_text, resolved_content: l.resolved_content,
        resolved_at: l.resolved_at, created_at: l.created_at,
    }).collect();
    let count = responses.len();
    Ok(Json(ContentLinkListResponse { content_links: responses, count }))
}

pub async fn delete_content_link(
    State(state): State<Arc<AppState>>,
    Path(link_id): Path<String>,
) -> Result<Json<serde_json::Value>, (StatusCode, Json<ErrorResponse>)> {
    let mut repo = state.repo.lock().await;
    match repo.delete_content_link(&link_id) {
        Ok(true) => Ok(Json(serde_json::json!({"deleted": true, "id": link_id}))),
        Ok(false) => Err((StatusCode::NOT_FOUND, Json(ErrorResponse {
            error: format!("Content link {} not found", link_id), code: 404,
        }))),
        Err(e) => Err((StatusCode::INTERNAL_SERVER_ERROR, Json(ErrorResponse {
            error: format!("Failed to delete content link: {}", e), code: 500,
        }))),
    }
}
```

- [ ] **Step 3: Register routes in `app()` function**

Add to the `Router::new()` chain before `.with_state(state)`:

```rust
.route("/documents/{document_id}/content-links", get(list_content_links).post(create_content_link))
.route("/documents/{document_id}/outbound-content-links", get(list_outbound_content_links))
.route("/content-links/{link_id}", delete(delete_content_link))
.route("/content-links/{link_id}/resolve", post(resolve_content_link))
```

- [ ] **Step 4: Add integration tests**

Add to `integration_test.rs`:

```rust
#[tokio::test]
async fn test_content_link_crud() {
    let state = storage_service::create_test_state();
    let app = storage_service::app(state.clone());

    // Create a source document via API
    let src_body = serde_json::json!({
        "name": "source-doc.txt",
        "content_type": "text/plain",
        "data": base64::Engine::encode(&base64::engine::general_purpose::STANDARD, b"Hello from source document!")
    });
    let src_resp = app
        .clone()
        .oneshot(
            Request::builder()
                .method(Method::POST)
                .uri("/files")
                .header("content-type", "application/json")
                .body(Body::from(serde_json::to_string(&src_body).unwrap()))
                .unwrap(),
        )
        .await
        .unwrap();
    assert_eq!(src_resp.status(), StatusCode::CREATED);
    let src_body: serde_json::Value = serde_json::from_slice(&hyper::body::to_bytes(src_resp.into_body()).await.unwrap()).unwrap();
    let src_id = src_body["file"]["id"].as_str().unwrap().to_string();

    // Create a target document
    let tgt_body = serde_json::json!({
        "name": "target-doc.txt",
        "content_type": "text/plain",
        "data": base64::Engine::encode(&base64::engine::general_purpose::STANDARD, b"Target content")
    });
    let tgt_resp = app
        .clone()
        .oneshot(
            Request::builder()
                .method(Method::POST)
                .uri("/files")
                .header("content-type", "application/json")
                .body(Body::from(serde_json::to_string(&tgt_body).unwrap()))
                .unwrap(),
        )
        .await
        .unwrap();
    assert_eq!(tgt_resp.status(), StatusCode::CREATED);
    let tgt_body: serde_json::Value = serde_json::from_slice(&hyper::body::to_bytes(tgt_resp.into_body()).await.unwrap()).unwrap();
    let tgt_id = tgt_body["file"]["id"].as_str().unwrap().to_string();

    // Create content link
    let cl_body = serde_json::json!({
        "source_document_id": src_id,
        "source_document_name": "Source Document",
        "target_document_name": "Target Document",
        "display_text": "See source doc"
    });
    let cl_resp = app
        .clone()
        .oneshot(
            Request::builder()
                .method(Method::POST)
                .uri(format!("/documents/{}/content-links", tgt_id))
                .header("content-type", "application/json")
                .body(Body::from(serde_json::to_string(&cl_body).unwrap()))
                .unwrap(),
        )
        .await
        .unwrap();
    assert_eq!(cl_resp.status(), StatusCode::CREATED);
    let cl_data: serde_json::Value = serde_json::from_slice(&hyper::body::to_bytes(cl_resp.into_body()).await.unwrap()).unwrap();
    let cl_id = cl_data["id"].as_str().unwrap().to_string();
    assert_eq!(cl_data["source_document_id"], src_id);
    assert_eq!(cl_data["target_document_id"], tgt_id);

    // List content links for target
    let list_resp = app
        .clone()
        .oneshot(
            Request::builder()
                .method(Method::GET)
                .uri(format!("/documents/{}/content-links", tgt_id))
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();
    assert_eq!(list_resp.status(), StatusCode::OK);
    let list_data: serde_json::Value = serde_json::from_slice(&hyper::body::to_bytes(list_resp.into_body()).await.unwrap()).unwrap();
    assert_eq!(list_data["count"], 1);

    // Delete content link
    let del_resp = app
        .clone()
        .oneshot(
            Request::builder()
                .method(Method::DELETE)
                .uri(format!("/content-links/{}", cl_id))
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();
    assert_eq!(del_resp.status(), StatusCode::OK);
}
```

- [ ] **Step 5: Build and test**

Run: `cargo test -p storage-service --lib && cargo test -p storage-service --test integration_test`
Expected: all tests pass

- [ ] **Step 6: Commit**

```bash
git add services/storage-service/src/lib.rs services/storage-service/tests/integration_test.rs
git commit -m "feat(storage): add ContentLink REST API routes with tests"
```

---

### Task 3: MCP server — ContentLink client methods

**Files:**
- Modify: `services/mcp-server/src/client.rs`

- [ ] **Step 1: Add `create_content_link`, `list_content_links`, `resolve_content_link` methods to `StorageClient`**

Add after the `list_mentions` method:

```rust
/// Create a content link from target document to source document.
pub async fn create_content_link(
    &self,
    target_document_id: &str,
    source_document_id: &str,
    source_document_name: &str,
    target_document_name: &str,
    display_text: &str,
) -> Result<serde_json::Value> {
    let body = serde_json::json!({
        "source_document_id": source_document_id,
        "source_document_name": source_document_name,
        "target_document_name": target_document_name,
        "display_text": display_text,
    });

    let resp = self
        .http
        .post(format!(
            "{}/documents/{target_document_id}/content-links",
            self.base_url
        ))
        .json(&body)
        .send()
        .await?;

    let status = resp.status().as_u16();
    if !resp.status().is_success() {
        let body = resp.text().await.unwrap_or_default();
        tracing::error!(status, %body, target_document_id, "create_content_link failed");
        return Err(StorageClientError::Status { status, body });
    }

    let data: serde_json::Value = resp.json().await?;
    Ok(data)
}

/// List content links for a document (inbound references).
pub async fn list_content_links(&self, document_id: &str) -> Result<serde_json::Value> {
    let resp = self
        .http
        .get(format!("{}/documents/{document_id}/content-links", self.base_url))
        .send()
        .await?;

    let status = resp.status().as_u16();
    if !resp.status().is_success() {
        let body = resp.text().await.unwrap_or_default();
        tracing::error!(status, %body, document_id, "list_content_links failed");
        return Err(StorageClientError::Status { status, body });
    }

    let data: serde_json::Value = resp.json().await?;
    Ok(data)
}

/// Resolve (re-fetch) a content link's source content.
pub async fn resolve_content_link(&self, link_id: &str) -> Result<serde_json::Value> {
    let resp = self
        .http
        .post(format!("{}/content-links/{link_id}/resolve", self.base_url))
        .send()
        .await?;

    let status = resp.status().as_u16();
    if !resp.status().is_success() {
        let body = resp.text().await.unwrap_or_default();
        tracing::error!(status, %body, link_id, "resolve_content_link failed");
        return Err(StorageClientError::Status { status, body });
    }

    let data: serde_json::Value = resp.json().await?;
    Ok(data)
}
```

- [ ] **Step 2: Build check**

Run: `cargo check -p mcp-server`
Expected: compiles without errors

- [ ] **Step 3: Commit**

```bash
git add services/mcp-server/src/client.rs
git commit -m "feat(mcp): add ContentLink client methods to StorageClient"
```

---

### Task 4: MCP server — ContentLink tool definitions + handlers

**Files:**
- Modify: `services/mcp-server/src/tools.rs`

- [ ] **Step 1: Add 3 tool definitions in `tool_definitions()`**

Add after the `list_mentions` tool:

```rust
// ── ContentLink tools ──
Tool::new(
    "create_contentlink",
    "Create a cross-document content link. Embeds a live reference from the target document to content in a source document. The resolved content stays in sync as the source document changes.",
    Arc::new(object(json!({
        "type": "object",
        "properties": {
            "target_document_id": { "type": "string", "description": "ID of the document to add the reference to" },
            "source_document_id": { "type": "string", "description": "ID of the document whose content to reference" },
            "source_document_name": { "type": "string", "description": "Human-readable name of the source document" },
            "target_document_name": { "type": "string", "description": "Human-readable name of the target document" },
            "display_text": { "type": "string", "description": "Optional display text for the link. Defaults to source document name." }
        },
        "required": ["target_document_id", "source_document_id", "source_document_name", "target_document_name"]
    }))),
),
Tool::new(
    "list_contentlinks",
    "List all content links (cross-document references) for a document, including resolved content previews",
    Arc::new(object(json!({
        "type": "object",
        "properties": {
            "document_id": { "type": "string", "description": "Document ID" }
        },
        "required": ["document_id"]
    }))),
),
Tool::new(
    "resolve_contentlink",
    "Re-fetch and cache the resolved content for a content link. Useful when the source document has been updated.",
    Arc::new(object(json!({
        "type": "object",
        "properties": {
            "link_id": { "type": "string", "description": "Content link ID" }
        },
        "required": ["link_id"]
    }))),
),
```

- [ ] **Step 2: Update `instructions` string in `get_info()`**

Change to include ContentLink tools:

```rust
instructions: Some(
    "Read, write, and manage World Office documents with automatic version snapshots. "
        .to_string()
        + "Comment on documents with @agent mentions and resolve threads. "
        + "Agents can check their @mentions to discover when they've been referenced. "
        + "Create cross-document content links to embed live references between documents.",
),
```

- [ ] **Step 3: Add 3 tool handlers in `call_tool()` match arm**

Add before the `other =>` catch-all:

```rust
// ── ContentLink tool handlers ──
"create_contentlink" => {
    let target_doc_id = Self::get_arg(&request.arguments, "target_document_id").ok_or_else(|| {
        ErrorData::invalid_params("Missing required: target_document_id", None)
    })?;
    let source_doc_id = Self::get_arg(&request.arguments, "source_document_id").ok_or_else(|| {
        ErrorData::invalid_params("Missing required: source_document_id", None)
    })?;
    let source_name = Self::get_arg(&request.arguments, "source_document_name").ok_or_else(|| {
        ErrorData::invalid_params("Missing required: source_document_name", None)
    })?;
    let target_name = Self::get_arg(&request.arguments, "target_document_name").ok_or_else(|| {
        ErrorData::invalid_params("Missing required: target_document_name", None)
    })?;
    let display_text = Self::get_arg(&request.arguments, "display_text").unwrap_or(source_name);

    match self.client.create_content_link(target_doc_id, source_doc_id, source_name, target_name, display_text).await {
        Ok(data) => Ok(CallToolResult::success(vec![Content::text(data.to_string())])),
        Err(e) => Ok(Self::error_result(e.to_string())),
    }
}
"list_contentlinks" => {
    let doc_id = Self::get_arg(&request.arguments, "document_id").ok_or_else(|| {
        ErrorData::invalid_params("Missing required: document_id", None)
    })?;
    match self.client.list_content_links(doc_id).await {
        Ok(data) => Ok(CallToolResult::success(vec![Content::text(data.to_string())])),
        Err(e) => Ok(Self::error_result(e.to_string())),
    }
}
"resolve_contentlink" => {
    let link_id = Self::get_arg(&request.arguments, "link_id").ok_or_else(|| {
        ErrorData::invalid_params("Missing required: link_id", None)
    })?;
    match self.client.resolve_content_link(link_id).await {
        Ok(data) => Ok(CallToolResult::success(vec![Content::text(data.to_string())])),
        Err(e) => Ok(Self::error_result(e.to_string())),
    }
}
```

- [ ] **Step 4: Build check**

Run: `cargo check -p mcp-server`
Expected: compiles without errors

- [ ] **Step 5: Commit**

```bash
git add services/mcp-server/src/tools.rs
git commit -m "feat(mcp): add ContentLink tools — create_contentlink, list_contentlinks, resolve_contentlink"
```

---

### Task 5: Frontend — ContentLink panel React components

**Files:**
- Create: `apps/web/apps/documenteditor-react/src/hooks/useContentLinks.ts`
- Create: `apps/web/apps/documenteditor-react/src/stores/ContentLinkStore.ts`
- Create: `apps/web/apps/documenteditor-react/src/components/ContentLinkPanel.tsx`
- Create: `apps/web/apps/documenteditor-react/src/components/ContentLinkList.tsx`
- Modify: `apps/web/apps/documenteditor-react/src/components/LeftMenu/LeftMenu.tsx`
- Modify: `apps/web/apps/documenteditor-react/src/App.tsx`

- [ ] **Step 1: Create `ContentLinkStore.ts`**

```typescript
import { makeAutoObservable } from "mobx"

export interface ContentLink {
  id: string
  source_document_id: string
  source_document_name: string
  target_document_id: string
  target_document_name: string
  display_text: string
  resolved_content: string
  resolved_at: string | null
  created_at: string
}

export class ContentLinkStore {
  links: ContentLink[] = []
  loading = false
  error: string | null = null
  documentId: string | null = null

  constructor() {
    makeAutoObservable(this)
  }

  setDocumentId(id: string | null): void {
    this.documentId = id
  }

  setLinks(links: ContentLink[]): void {
    this.links = links
  }

  setLoading(loading: boolean): void {
    this.loading = loading
  }

  setError(error: string | null): void {
    this.error = error
  }
}

export const contentLinkStore = new ContentLinkStore()
```

- [ ] **Step 2: Create `useContentLinks.ts` hook**

```typescript
import { useEffect, useCallback } from "react"
import { contentLinkStore, type ContentLink } from "../stores/ContentLinkStore"

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8002"

export function useContentLinks(documentId: string | null) {
  useEffect(() => {
    contentLinkStore.setDocumentId(documentId)
    if (!documentId) {
      contentLinkStore.setLinks([])
      return
    }

    let cancelled = false
    contentLinkStore.setLoading(true)
    contentLinkStore.setError(null)

    fetch(`${API_BASE}/documents/${documentId}/content-links`)
      .then((res) => {
        if (!res.ok) throw new Error(`Failed to fetch: ${res.status}`)
        return res.json()
      })
      .then((data: { content_links: ContentLink[] }) => {
        if (!cancelled) {
          contentLinkStore.setLinks(data.content_links)
          contentLinkStore.setLoading(false)
        }
      })
      .catch((err: Error) => {
        if (!cancelled) {
          contentLinkStore.setError(err.message)
          contentLinkStore.setLoading(false)
        }
      })

    return () => {
      cancelled = true
    }
  }, [documentId])

  const resolveLink = useCallback(async (linkId: string) => {
    try {
      const res = await fetch(`${API_BASE}/content-links/${linkId}/resolve`, {
        method: "POST",
      })
      if (!res.ok) throw new Error(`Failed to resolve: ${res.status}`)
      const updated: ContentLink = await res.json()
      contentLinkStore.setLinks(
        contentLinkStore.links.map((l) => (l.id === linkId ? updated : l)),
      )
    } catch (err: unknown) {
      contentLinkStore.setError(
        err instanceof Error ? err.message : "Failed to resolve",
      )
    }
  }, [])

  return { store: contentLinkStore, resolveLink }
}
```

- [ ] **Step 3: Create `ContentLinkList.tsx`**

```tsx
import React from "react"
import type { ContentLink } from "../stores/ContentLinkStore"

interface ContentLinkListProps {
  links: ContentLink[]
  loading: boolean
  onResolve: (id: string) => void
  onNavigate: (docId: string) => void
}

export const ContentLinkList: React.FC<ContentLinkListProps> = ({
  links,
  loading,
  onResolve,
  onNavigate,
}) => {
  if (loading) {
    return <div className="cl-loading">Loading content links...</div>
  }

  if (links.length === 0) {
    return (
      <div className="cl-empty">
        <p>No content links in this document.</p>
        <p className="cl-hint">
          Agents can create content links via MCP tools to reference content from other documents.
        </p>
      </div>
    )
  }

  return (
    <div className="cl-list">
      {links.map((link) => (
        <div key={link.id} className="cl-item">
          <div className="cl-header">
            <span className="cl-source" title={link.source_document_id}>
              {link.source_document_name}
            </span>
            <span className="cl-arrow">→</span>
            <span className="cl-target">{link.target_document_name}</span>
          </div>
          {link.display_text && (
            <div className="cl-display-text">{link.display_text}</div>
          )}
          {link.resolved_content && (
            <div className="cl-resolved-preview">
              <div className="cl-preview-label">Content Preview:</div>
              <div className="cl-preview-text">{link.resolved_content}</div>
            </div>
          )}
          {link.resolved_at && (
            <div className="cl-resolved-at">
              Last resolved: {new Date(link.resolved_at).toLocaleString()}
            </div>
          )}
          <div className="cl-actions">
            <button
              className="cl-btn cl-btn-resolve"
              onClick={() => onResolve(link.id)}
              title="Re-fetch source content"
            >
              Refresh
            </button>
            <button
              className="cl-btn cl-btn-navigate"
              onClick={() => onNavigate(link.source_document_id)}
              title="Open source document"
            >
              Open Source
            </button>
          </div>
        </div>
      ))}
    </div>
  )
}
```

- [ ] **Step 4: Create `ContentLinkPanel.tsx`**

```tsx
import React, { useCallback } from "react"
import { observer } from "mobx-react-lite"
import { useContentLinks } from "../hooks/useContentLinks"
import { contentLinkStore } from "../stores/ContentLinkStore"
import { ContentLinkList } from "./ContentLinkList"

interface ContentLinkPanelProps {
  documentId: string | null
}

export const ContentLinkPanel: React.FC<ContentLinkPanelProps> = observer(
  ({ documentId }) => {
    const { store, resolveLink } = useContentLinks(documentId)

    const handleNavigate = useCallback((docId: string) => {
      // In a real editor, this would navigate to the document
      // For V1 we open the storage service's file metadata page
      window.open(
        `${import.meta.env.VITE_API_URL || "http://localhost:8002"}/files/${docId}`,
        "_blank",
      )
    }, [])

    return (
      <div className="cl-panel">
        <div className="cl-panel-header">
          <h3>Content Links</h3>
          <span className="cl-count">{store.links.length} reference(s)</span>
        </div>
        <ContentLinkList
          links={store.links}
          loading={store.loading}
          onResolve={resolveLink}
          onNavigate={handleNavigate}
        />
        {store.error && (
          <div className="cl-error">Error: {store.error}</div>
        )}
      </div>
    )
  },
)
```

- [ ] **Step 5: Update `LeftMenu.tsx` to add ContentLink button**

Find the `LeftMenuAction` type definition in `types/document.ts` and add `"contentlinks"`:

```typescript
export type LeftMenuAction =
  | "search"
  | "comments"
  | "chat"
  | "navigation"
  | "thumbnails"
  | "support"
  | "about"
  | "contentlinks"     // ← add this
```

In `LeftMenu.tsx`, add a button for content links after the comments button:

```tsx
<LeftMenuButton
  action="contentlinks"
  icon="🔗" // Replace with actual icon component
  tooltip="Content Links"
  isActive={activeLeftPanel === "contentlinks"}
  onClick={() => toggleLeftPanel("contentlinks")}
/>
```

In `LeftMenuButton.tsx`, add mapping for the new action if needed.

In `App.tsx`, render the `ContentLinkPanel` when `activeLeftPanel === "contentlinks"`:

```tsx
{activeLeftPanel === "contentlinks" && (
  <ContentLinkPanel documentId={currentDocumentId} />
)}
```

- [ ] **Step 6: Build check**

Run: `pnpm lint && pnpm typecheck` from server root
Expected: no errors

- [ ] **Step 7: Commit**

```bash
git add apps/web/apps/documenteditor-react/src/hooks/useContentLinks.ts apps/web/apps/documenteditor-react/src/stores/ContentLinkStore.ts apps/web/apps/documenteditor-react/src/components/ContentLinkPanel.tsx apps/web/apps/documenteditor-react/src/components/ContentLinkList.tsx apps/web/apps/documenteditor-react/src/types/document.ts
git commit -m "feat(web): add ContentLink React panel, store, and hook for cross-document references"
```

---

### Task 6: E2E tests + verification

**Files:**
- Run: full test suite

- [ ] **Step 1: Run Rust tests**

```bash
cargo test -p storage-service --lib  # repository tests
cargo test -p storage-service --test integration_test  # API tests
cargo check -p mcp-server  # MCP server compiles
```

Expected: all pass

- [ ] **Step 2: Run TypeScript checks**

```bash
pnpm lint
pnpm typecheck
```

Expected: no errors

- [ ] **Step 3: Run full workspace check**

```bash
cargo check --workspace
```

Expected: 0 errors

- [ ] **Step 4: Update ROADMAP.md**

Mark MCP Server + Version Snapshots as done. Mark ContentLink as in progress.

- [ ] **Step 5: Final commit**

```bash
git add .
git commit -m "docs: update ROADMAP for ContentLink sprint"
```
