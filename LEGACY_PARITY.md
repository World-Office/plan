# Legacy-Codebase-Parität (opencloud-docserver → rust docserver)

Generiert 2026-10-13T19:13:00 aus dem wo-test-harness (`census/legacy/`). Vier Achsen: UI-Marker, API-Fläche, Behavior, Contract-Mining.

## Kernaussage

**Kein Regressionssignal.** Der Rust-Port ist auf allen drei Achsen Superset oder identisch zur legacy python codebase. Der Restwert der legacy codebase liegt NICHT in verlorenen Features, sondern in ihrem Verhaltens-Korpus: 134 e2e-Testdateien (1627 Testfunktionen) sind fertige Verhaltens-Spezifikationen, aus denen Parity-Contracts gehoben werden können.

## 1. UI-Marker (web/ vs documenteditor-wysiwyg/)

| Achse | legacy | current | verloren | neu |
|---|---|---|---|---|
| control-ids | 273 | 273 | 0 | 0 |
| data-cmds | 12 | 17 | 0 | 5 |
| i18n-keys | 240 | 240 | 0 | 0 |
| dialog-ids | 40 | 40 | 0 | 0 |

## 2. API-Fläche (FastAPI vs axum)

legacy 36 Routen, current 36, legacy-only 4 (4 davon durch Wildcard-Handler abgedeckt).
- `/wopi/files/{id}/getlock` → abgedeckt durch `/hosting/wopi/{*path}` (hosting_wopi_handler)
- `/wopi/files/{id}/lock` → abgedeckt durch `/hosting/wopi/{*path}` (hosting_wopi_handler)
- `/wopi/files/{id}/refreshlock` → abgedeckt durch `/hosting/wopi/{*path}` (hosting_wopi_handler)
- `/wopi/files/{id}/unlock` → abgedeckt durch `/hosting/wopi/{*path}` (hosting_wopi_handler)

## 3. Behavior (editor.js Funktionsinventar)

legacy 315 Funktionen, current 327. legacy-only: **0**, current-only: 12 (Weiterentwicklung).

| Keyword | legacy | current |
|---|---|---|
| pagination | 40 | 44 |
| pageFurniture | 8 | 8 |
| conversion | 110 | 110 |
| collab | 115 | 116 |
| protection | 153 | 153 |

## 4. Contract-Mining: legacy e2e als Spec-Quelle

Legacy-Korpus: 134 Dateien, 1627 Testfunktionen. Hebungspfad: je Test ein Verhaltens-Contract (assertion.kind dom-mutation/op-emitted/dialog-visible) in word-parity-overrides.json — die UI-Marker existieren alle bereits in der aktuellen UI (Achse 1).

| Datei | Tests | Thema |
|---|---|---|
| test_auth_gui.py | 4 | Authentication & shell GUI tests — the front door of the cloud. |
| test_button_sweep_gui.py | 15 | Button sweep: every button in the cloud UI shell gets exercised. |
| test_document_edit_depth.py | 7 | Deep document-editing semantics against the LIVE docserver. |
| test_editor_depth_gui.py | 6 | Depth tests for the embedded word editor: keyboard, layout, lifecycle. |
| test_editor_menu_gui.py | 4 | Editor File-menu chrome against the DEPLOYED bundle. |
| test_editors_gui.py | 6 | Editor-opening tests: every office type must open an editor via the GUI. |
| test_file_lifecycle.py | 8 | File lifecycle edge cases: odd names, dotfiles, moves, overwrites, sizes. |
| test_files_depth_gui.py | 6 | Files-app depth: search, details sidebar, view modes, trash, open-with. |
| test_files_gui.py | 6 | Files-app GUI tests: create / rename / delete / navigate, plus WebDAV parity. |
| test_multisession_gui.py | 1 | Multi-session GUI tests: the same document opened from two browser contexts. |
| test_paper_collaboration.py | 16 | The scientist-collaboration scenario, end to end. |
| test_protocol_depth.py | 6 | Protocol robustness: hard negatives and concurrency for the live docserver. |
| test_share_lifecycle.py | 7 | Share lifecycle: grants, revocations, link protection, reshare control. |
| test_toolbar_sweep_graph.py | 2 | Graph-driven toolbar sweep (button sweep 2.0). |
| test_wopi_protocol.py | 6 | WOPI protocol-level tests against the live docserver (no browser). |
| test_word_editing_gui.py | 5 | Word-editor interaction tests — the full editing experience via the GUI. |
| bench/test_converter_perf.py | 4 | Performance-regression tests for the DOCX <-> HTML converter. |
| e2e/test_a11y_keyboard.py | 8 | E2E — Keyboard-Navigation accessibility (test-a11y-keyboard). |
| e2e/test_cloud_editor_e2e.py | 30 | End-to-end cloud editor test (T5). |
| e2e/test_collab_sync.py | 6 | E2E — Realtime-Text-Sync (US-42, contract: docs/testing/test-scenarios.md). |
| e2e/test_full_workflow.py | 5 | E2E — Vollständiger Workflow (complete production workflow). |
| e2e/test_headings_opencloud.py | 6 | E2E — heading styles through production OpenCloud (OCIS client mode). |
| e2e/test_image_upload.py | 7 | E2E — Bild-Einsetzen via Upload (insert image with upload dialog). |
| e2e/test_images_opencloud.py | 6 | E2E — images through production OpenCloud (OCIS client mode). |
| e2e/test_lists_opencloud.py | 6 | E2E — lists through production OpenCloud (OCIS client mode). |
| e2e/test_odt_opencloud.py | 5 | E2E — ODT document through production OpenCloud (OCIS client mode). |
| e2e/test_ribbon_geometry.py | 1 | E2E — ribbon geometry gate (fast drift catcher, no screenshots). |
| e2e/test_tables_opencloud.py | 7 | E2E — tables through production OpenCloud (OCIS client mode). |
| test_agent_collab_interleave.py | 4 | Tests for interleaved human and agent operations in the docserver. |
| test_agent_loop_integration.py | 11 | Full agent loop integration tests — scripted model edits converge (INT+PROP). |
| test_ai_adapters.py | 7 | Provider adapters (E19S1): vendor-agnostic tool-call translation. |
| test_ai_agent_edits.py | 3 | Agent edits preserve document integrity — property-based (eval harness). |
| test_ai_agent_modelbased.py | 4 | Model-based testing of the agent state machine driving apply_ops (TC-E13-05). |
| test_ai_agent_sanitizer.py | 3 | Agent path under the sanitizer contract (E17S4): agent-authored content |
| test_ai_anchor_ops.py | 10 | Anchored agent edits (E18S2): set_span + expected CAS — precision beats rewrite. |
| test_ai_audit.py | 6 | Agent run audit (E20): every agent turn leaves a queryable row. |
| test_ai_context_pack.py | 8 | Grounding pack (get_context, E18S1): deterministic, size-bounded, isolated. |
| test_ai_injection_containment.py | 4 | Prompt-injection containment (E17): document content is DATA, never a |
| test_ai_lock_parity.py | 11 | Property-based tests for lock-tool / WOPI lock-parity. |
| test_ai_mcp.py | 10 | MCP stdio server: protocol handling and hostile-input resilience. |
| test_ai_mcp_catalog.py | 17 | MCP tool catalog discovery and schema completeness. |
| test_ai_mcp_fuzz.py | 7 | FUZZ: hostile doc-ids and arguments against the MCP tool surface. |
| test_ai_no_egress.py | 2 | Egress guard (E17S5) + local-model E2E (E19S2). |
| test_ai_ops_validation.py | 4 | Malformed agent operations are rejected gracefully, hub never crashes. |
| test_ai_permissions.py | 7 | Agent permission scope, consent fail-closed, and confused-deputy guards. |
| test_ai_propose.py | 5 | AI propose endpoint: instruction -> applied ops (flagship v3-1). |
| test_ai_provider_fail.py | 8 | Provider callable failure modes: raises/times out — typed error, document uncorrupted. |
| test_ai_review.py | 6 | AI review endpoints: op-stream diff, per-op reject, reject-all. |
| test_ai_review_control.py | 11 | Tests for reject_agent_ops inverse ops restore pre-agent state (TC-E16). |
| test_ai_runner.py | 7 | AgentRunner: model-agnostic loop, budgets (runaway protection), attribution. |
| test_ai_runner_bounds.py | 15 | Agent loop budget enforcement: runaway loop protection (TC-E17-05/06). |
| test_ai_search_doc.py | 6 | Cited retrieval (search_doc, E18S3): deterministic passage ranking. |
| test_ai_tools.py | 26 | Agent tool surface: discovery, contracts, and hostile-input hardening. |
| test_ai_tools_edge.py | 23 | Agent tool surface: edge cases for reads, versions, presence, typed not-found. |
| test_ai_traces.py | 8 | Structured agent traces (E20S1): redacted by default, retention-bounded. |
| test_api_error_shapes.py | 7 | API error-shape sweep: structured typed errors across every route family. |
| test_api_fuzz.py | 2 | Route/API fuzzing — the whole HTTP surface must never crash. |
| test_chat_panel.py | 9 | TDD test for chat panel UI (collab.chat feature). |
| test_cli.py | 12 | Unit tests for docserver CLI — arg parsing, dispatch, exit codes. |
| test_client_mode.py | 13 | Tests for OCIS client mode: editor sessions + remote WOPI client. |
| test_collab.py | 36 | Tests for the real-time collaboration layer (character CRDT + hub + API). |
| test_collab_concurrency.py | 4 | Tests for Hub concurrency: parallel sites op-flood, revision continuity, and no lost ops. |
| test_collab_modelbased.py | 0 | Stateful model-based testing of the TextCRDT collaboration core. |
| test_config_precedence.py | 25 | Tests for configuration precedence: env overrides toml overrides defaults. |
| test_config_validation.py | 6 | Unit tests for config validation in ``src.config``. |
| test_conformance_corpus.py | 1 | Borrow the World-Office ``wo-conformance`` corpus as round-trip coverage. |
| test_converter.py | 99 | Tests for DOCX <-> HTML conversion. |
| test_converter_differential.py | 2 | Differential testing of the docserver converters against LibreOffice. |
| test_converter_notes_bookmarks.py | 10 | Tests for converter.py notes/bookmarks/tables coverage. |
| test_converter_property.py | 6 | State-of-the-art converter testing: property-based + metamorphic + fuzz. |
| test_converter_roundtrip_text.py | 4 | Property-based tests for text preservation across DOCX and ODT round-trips. |
| test_converter_run_style_edges.py | 84 | Tests for converter.py run-level HTML edges: _run_to_html/_apply_run_style formatting comb |
| test_crdt_concurrent_edges.py | 4 | Tests for TextCRDT concurrency edges: same-position inserts, delete idempotence, and tombs |
| test_crypto.py | 4 | Tests for JWT token helpers. |
| test_crypto_edges.py | 4 | Tests for token crypto edge cases: TTL, wrong secret, and tampering. |
| test_document_info.py | 4 | Document info / metadata endpoint (F-006). |
| test_document_protection.py | 15 | Document protection: protect.password + protect.restrict (engine wo-feature). |
| test_draw_select.py | 6 | TDD test for Draw tab stroke select + delete/move (WO-FEA-DRAW-2). |
| test_draw_tools.py | 13 | TDD test for Draw tab tools (WO-FEA-DRAW-1). |
| test_editor_api_lifecycle.py | 20 | Documents REST lifecycle: new→contents→save→versions→restore + typed 404. |
| test_editor_export.py | 10 | API tests for the editor export endpoints (html/odt/docx). |
| test_editor_router_edges.py | 24 | Editor router edge cases and error branches. |
| test_export.py | 4 | TDD tests for cloud-integration export endpoints (editor-cloud-ui T1-T3). |
| test_export_formats.py | 10 | Export & download endpoints (F-002 Download as ODT, F-003 Download as DOCX, |
| test_file_menu.py | 18 | TDD test for File-Menu UI (editor-cloud-ui T6). |
| test_file_ops.py | 3 | Tests for file operations: export (ODT/HTML) and the new-document route. |
| test_find_replace.py | 4 | feature register: F-062 F-063 F-064 |
| test_font_controls.py | 7 | Feature Register Coverage: F-018 F-019 F-020 F-021 F-022 F-023 F-024 |
| test_format_spec_conformance.py | 9 | Format-spec conformance for engine-produced DOCX and ODT artifacts |
| test_ink_canvas.py | 6 | TDD test for Draw tab ink canvas layer (WO-FEA-DRAW-0). |
| test_insert_advanced.py | 17 | Tests for insert features: image, textbox, shape, chart, header/footer, page numbers, equa |
| test_layout_roundtrip.py | 6 | Feature Register Tests: |
| test_main_bootstrap.py | 4 | Unit tests for app bootstrap — routers, CORS, and lifespan. |
| test_main_surface.py | 16 | App shell surface: /health payload, / index HTML, /static mount, traversal 404 shapes. |
| test_markers.py | 31 | Section-flag + drop cap + borders round-trip tests. |
| test_new_doc.py | 2 | TDD tests for new-document endpoint (editor-cloud-ui T4-T5). |
| test_odt_converter.py | 82 | Tests for ODT <-> HTML conversion. |
| test_odt_media_pipeline.py | 8 | ODT media pipeline internals: MIME sniffing, JPEG SOF parsing, data-URI |
| test_odt_tables_frames.py | 12 | ODT converter: table spans+borders, draw:frame image/textbox, tracked changes. |
| test_onlyoffice_conformance.py | 27 | ONLYOFFICE-informed conformance tests for the editor-format features. |
| test_page_break_roundtrip.py | 5 | Page break roundtrip: editor marker <-> DOCX/ODT serialization (F-076). |
| test_page_setup.py | 7 | Page setup round-trip tests (F-090 page size / F-091 orientation / F-092 margins). |
| test_paragraph_controls.py | 14 | Paragraph controls: multilevel lists (F-032) and line spacing (F-039). |
| test_persistence.py | 12 | Persistence, crash-recovery and exactly-once retry semantics. |
| test_plugin_host.py | 5 | TDD test for Plugin Host UI (plugins.browse / plugins.manage). |
| test_plugin_ocr.py | 6 | TDD test for OCR plugin UI (plugins.ocr feature). |
| test_plugin_photoeditor.py | 6 | TDD test for the Photo Editor plugin — canvas filter dialog |
| test_ref_fields.py | 10 | Citation + Index L1 field marker tests (ref.citation / ref.index). |
| test_resilience.py | 15 | Resilience and fault-injection testing of the docserver. |
| test_review_surfaces.py | 16 | Review surfaces: track changes, accept/reject, comments, version history. |
| test_sanitize_review_edges.py | 24 | Edge units across the hostile-input + review + MCP surface. |
| test_sanitizer_adversarial.py | 4 | Adversarial security tests for the HTML sanitizer. |
| test_sanitizer_agent_html.py | 13 | Sanitizer tests for agent-authored hostile HTML (SEC+FUZZ). |
| test_session_lock_adoption.py | 11 | Editor-session lock adoption against the stub WOPI host + SessionRegistry semantics. |
| test_session_lock_edges.py | 19 | Tests for session/lock adoption branches + collab char_at/set_presence gaps. |
| test_session_registry.py | 9 | Tests for the ``SessionRegistry`` lifecycle. |
| test_snapshot_golden.py | 3 | Golden-master (snapshot) tests for the wire contracts. |
| test_store.py | 7 | Tests for the SQLite document store. |
| test_store_crash.py | 8 | DocumentStore crash-consistency: reopen mid-lifecycle, torn writes, oversize. |
| test_store_multi_instance.py | 8 | Multi-instance store: two DocumentStore handles on one dir stay consistent. |
| test_tracked_navigation.py | 5 | Wiring test for tracked-change prev/next navigation (collab.prev-change / |
| test_version_restore_semantics.py | 8 | Version-history semantics: monotonic listing, restore-to-old, immutability. |
| test_versions.py | 7 | Version history: store snapshots + editor API (T30, version-history). |
| test_view_controls.py | 9 | View-cluster controls: zoom, fullscreen, dark theme (and audit of fit/rulers). |
| test_web_surface.py | 9 | Web surface: hosting discovery XML, /editor page, /static assets content-types (UNIT). |
| test_wopi.py | 142 | Tests for WOPI host endpoints and editor API (integration style). |
| test_wopi_auth.py | 16 | Direct unit tests for the WOPI auth module — token lifecycle (UNIT). |
| test_wopi_checkfileinfo.py | 25 | Tests for CheckFileInfo contract: metadata fields, unicode names, read-only enforcement (U |
| test_wopi_host_integration.py | 2 | Integration test: docserver acts as WOPI client to a mock OpenCloud/Nextcloud host. |
| test_wopi_lock_lifecycle.py | 10 | WOPI lock lifecycle matrix: Lock / PutFile / Unlock / RefreshLock / GetLock (UNIT). |
| test_wopi_protocol_edge.py | 24 | WOPI protocol edge cases: malformed headers, unicode names, CheckInOut (UNIT). |
| test_wopi_protocol_property.py | 8 | Model-based and adversarial tests for the WOPI protocol boundary. |
| test_wopi_router_edges.py | 21 | WOPI router edge cases: MAX_FILE_SIZE, foreign lock ops, GetLock (UNIT). |
| test_wopi_testhost.py | 20 | Unit tests for the mock WOPI host (src/wopi/testhost.py) protocol surface. |

