# Parity backlog — WO editor vs OnlyOffice (deferred + skipped items)

**Source:** `wo-test-harness/census/ledger.json` (status `deferred`) + session next-steps.
**Gate:** `reconcile.py --check` (deferred must be 0).
**Result (2026-08-21):** parity debt **0** — gate PASS, real 119, covered 152, deferred 0.

## OO-parity deferred items — ALL DONE

- [x] spellcheck-language-future-iteration (12 rows) → statusbar `doc-lang` driven
- [x] react-filemenu-* (5: info/protect/settings/help/suggest) → File backstage dialogs
- [x] io-future-iteration (`text-fromfile`) → Insert > Text from File (+ host import-docx endpoint)
- [x] tts/stt (`speech speechinput`) → View > Speech (browser TTS/STT)
- [x] mailmerge → Insert > Mail merge wizard (CSV → fields → preview)
- [x] single-page-view → statusbar multiple-pages gutter view
- [x] text-marking-entry (`add-text`) → Insert > Add text mask
- [x] background-plugins → Plugins > Background mode
- [x] host-layer-permissions (asc-gen541/546) → covered by protection dialog
- [x] content-controls → Insert > Content control (plain/rich/dropdown)
- [x] field-codes + field engines (`insertfield asc-gen887 asc-gen889`) → Insert > Field dialog
- [x] float-layout (align/wrapping/bringforward/sendbackward) → object-layout popup
- [x] canvas group/merge (`group mergeshapes`) → Draw > Group / Merge shapes
- [x] no-canvas-layer (asc-gen668/670) → covered by draw ink canvas
- [x] equation → Insert > Equation (linear → SVG → PNG)
- [x] smartart → Insert > SmartArt gallery (4 templates)
- [x] chart-editing (8 rows) → Insert > Chart editor (type/data grid → SVG → PNG)

- [x] DrawingML chart engine (hand-rolled, zero libs): Chart imgs save as real
      OPC parts (word/charts/chartN.xml + content type + rel + c:chart ref).
      Bar/line/pie/area, title+data; reader parses the part back to the
      editable spec. Validated in LibreOffice (renders + survives re-export).
- [x] OMML equation engine (hand-rolled): linear ^/sub/fraction/sqrt ->
      m:oMathPara (paragraph-level placement — inside w:r is invalid and
      silently dropped by Word/LO). Reads back to the equation marker.

- [x] Pre-existing trio closed — full suite 1701 passed / 0 failed:
      (1) a11y keyboard: Styles menu buttons lacked aria-pressed so the mirror
      never touched them (real markup bug) — declared aria-pressed=false.
      (2) ai-503: e2e cloud test leaked 'default' into the shared MODEL_REGISTRY,
      only popped when the e2e file ran first — added finally cleanup.
      (3) check_file_info golden: python-docx 1.1->1.2 drift changed seed Size —
      pinned python-docx==1.2.0 + regenerated (diff = Size line only, now reproducible).
      Commit 1ae99fc20.

## Session next-steps

- [x] Wire `require_auth` into `src/wopi/router.py` — config-gated gate
      (`require_wopi_auth` / `DOCSERVER_REQUIRE_WOPI_AUTH`), 401 on missing/bad
      token when enforced, off by default (host mode = local-store trust
      boundary; the real OpenCloud client path already authenticates). 4 tests.
- [x] OMML/field engine: Insert > Field now round-trips as live `w:fldSimple`
      (safe instr allowlist) both directions — insert -> save -> reopen stays
      a field.
- [x] Content controls: `w:sdt` round-trip both directions (alias+tag).
- [x] True text-flow float: obj-square/obj-right/obj-behind -> anchored
      `w:drawing` (wp:anchor + wrapSquare/wrapBehind), W order preserved.
- [x] Post-insert vector re-edit: chart/equation/smartart carry data-spec +
      `__wo-<kind>__` alt marker (survives DOCX via docPr descr); double-click
      reopens the prefilled dialog. hydrateVectorObjects on load/undo.
- [x] Archive `plan/taskfleet/` → documented deprecated in-plan (`DEPRECATED.md`).
- [x] Restart staging `collaboration` for clean info logging.
- [x] Clean `/tmp` debug junk.

## Engine session 2026-10-31 (fresh census + engine slices)

- [x] Fresh census + parity ledger rebuild (harness `954b533`): L0 22→20.
      `page.none`/`page.automatic` were OO hyphenation menu items, not
      page-background — now L1 via `toggleHyphenation` (scoped fallback in
      `build.py`). Honest L0 floor = 12 ctx (CSS/vector/OLE-bound) + 7
      Chromium/Mac shortcuts + 1 OLE menu-item. Ledger L0/L1/L3 = 20/466/15.
- [x] Chart dataTable pageerror fix (server `d403c6b09`): chartSVG used
      undeclared showDataTable/dataTableH/tableRows — any legend-enabled chart
      threw ReferenceError. Declared + added the missing `chartElement
      dataTable` toggle. Plus 5 af-merge gate breaks repaired (Cyrillic ToF
      keys, Dialog.Ok, DIALOG_IDS entries, shape i18n, insertToF→
      insertTableOfFigures canonicalization, btn-field placement).
      Suite 105/105 → 106/106.
- [x] **C5-3 table formulas `=SUM(ABOVE)`** (server `3ea301383`): Table ops →
      Formula… dialog (SUM/AVERAGE/COUNT/MAX/MIN × ABOVE/BELOW/LEFT/RIGHT),
      `data-formula` cell engine, live recalc on table structure + cell edits,
      clear-on-overtype. Gate `table-formula.test.mjs` incl. verbatim-mirror
      behavior check. OO census has no formula capture → own engine slice,
      not a parity row. Documented ceiling: full-range scan (OO stops at
      blanks).
- [x] C8 equations gap check: **no gap** — all 5 ledger rows L1
      (btn-equation, Ctrl+Alt+=, ctx EquationSettings).
- [x] Prod deploy + sweep after each: 0 pageerrors. All pushed (server fleet+
      github), harness `954b533`.

## T-006 roundtrip extension — DONE (2026-11-01)

- [x] Probes 13 -> 21 (alignment x4, ul/ol lists, hyperlink, <hr>), 21/21
      survived; ledger L3 15 -> 24 (9 more features proven to persist:
      bullets, numbering, align-left/center/right/full, insert/references
      link, ctx.horizontal-line-settings). Harness `e5b4fcb`.
- [x] Two REAL data-loss bugs caught + fixed in the Rust converter
      (server `ad7528d06`): (1) html->docx dropped a <p> containing
      <ul>/<ol> — parser now HTML5-hoists nested blocks out of <p>;
      (2) <hr> saved as a 24x U+2500 garbage run — now a border-only
      paragraph (w:pBdr all four sides) that round-trips back to <hr/>.
      wo-html 113/113, wo-x2t 439/439. Deployed prod + staging, live
      round-trips verified (no garbage, <hr> survives).

## T-008 divergence rows — DONE (2026-11-01)

- [x] Officially-parked capability planes registered as LOUD divergences
      (harness `a37d5ab`): macros own-project (plan C12) + capability plane
      (C13) + forms-as-own-epic. Declared in interact-divergences.json
      (asc-gen937/939/4556), interact-diff.py promotes declared organic
      rows to `divergence`, interact-ledger rows flipped, and build.py
      `REGISTERED_PARKS` marks macros.* + plugins.plugin-manager as
      divergence:registered with park-reason evidence on every rebuild.
      Verified: ledger-gap collect_gaps surfaces them as divergence class —
      the af AI triage classifies them intentional (never work).

## Census refresh — DONE (2026-11-01)

- [x] Fresh WO inventory captured against live prod (harness `478f429`,
      00:02 UTC): buttons/dialogs/deep/shortcuts/interactions/ctx. Delta:
      table-ops now carries 'Formula…' (C5-3), bookmark gained data-cmd.
      Ledger rebuilt UNCHANGED at honest floor (L0=20, L1=457, L3=24;
      roundtrip 21/21). OO has ZERO formula mentions across all captures ->
      formula stays an unmeasured feature (C5-3 own gate). af loop REMAINS
      parked (61 parked rows, no new actionable rows; re-arm only when real
      new gaps appear). Legacy census/census/ledger.json re-synced.

## Phase 4 af campaign — DONE (2026-11-01, server `5947d034a`, harness `2d06e03`)

Run via af (3 tasks, all merged attempt-1, empty drain):
- [x] **insert-spreadsheet (OLE)** — Insert tools > Spreadsheet menuitem →
      openObjectDialog("spreadsheet") → OLE placeholder `data-type=spreadsheet`;
      option added to #object-type, i18n Insert.Spreadsheet en+de. Ledger
      `insert.insert-spreadsheet` L0→L1 (menu:btn-insert-more).
- [x] **NonBreakingHyphen** — Ctrl+Shift+Minus = U+2011 (OO true). Dash-trio
      root-cause fix: En dash moved to Ctrl+Minus (preventDefault blocks
      browser zoom-out) → `shortcut.nonbreakinghyphen` AND `shortcut.endash`
      both re-scored matched. shortcuts-gate 26 pins still pass.
- [x] **wo-renderer-wasm lib-test fix** — DocxBody `..Default::default()` in
      table_interaction_tests.rs + navigation_tests.rs (E0063 missing
      fields) → `cargo test -p wo-renderer-wasm --lib` 153/153.
- [ ] ~~backstage-shape divergences~~ — NOT ACTIONABLE: no shape items exist
      in either OO or WO backstage census captures; follow-up was vague
      shorthand, nothing to do.
Full editor suite 108/108; deployed prod+staging (shared static mount),
md5-verified, prod sweep 0 pageerrors. **L0 floor 20 → 18**
(501 {L0:18, L1:459, L3:24}; roundtrip 21/21). Af loop: still parked
(nothing new actionable); state-p4 receipts all merged.

## Phase 5 — the final 18 L0 rows via af — DONE (2026-11-01, server `24df0680d`, harness `6a6b1ac`)

Root cause of the dry loop: `ledger-gap.py collect_gaps()` only feeds the
legacy/interact buckets — the 18 level-based L0 rows never entered the
queue. Fix: hand-wrote honest specs for all 18 (dot-free slugs, receipt
regex `^WO-(\d+)-([\w-]+)` breaks on dots) directly into `ledger-gap.md`;
`wo-gen-round.py` parses it without AI triage. Re-armed `wo-loop.service`.

- **Batch 21 (10 ctx rows) — 10/10 merged.** distribute columns/rows (real
table equalizers; `70d6f064a` extended the direct-main agent commit `e00332b8f`
with colgroup `<col>` handling — no duplication), distribute horizontally/
vertically (shift-click multi-select + equal gaps), edit-object (object-dialog
prefilled, updates placeholder in place), convert-to-shape (shape picker
replaces placeholder), in-front-of-text/through/tight (obj-front/obj-through
classes + data-wrap), resize-to-cell (cell content-box). 2 had treat-to-fix
parallel-merge race failures (rows, horiz, columns, edit-object, through) —
all recovered on retry; one agent (local-dsv4) wrote main directly once
(safe: feature + test committed to HEAD, af later merged its own cleaner
colgroup impl on top).
- **Batch 22 (8) — 8/8 merged, all attempt 1.** 2 registered divergences
(edit-points / edit-wrap-boundary — no vector contour model → LOUD ctx rows:
wo: markers + SetStatus NotAvailable), 6 shortcuts (Cmd/Ctrl+W close-doc,
Cmd/Ctrl+O open, Ctrl+Alt+F file panel, Opt+Cmd+A comment, Opt+Cmd+X unicode-
escape→symbol, Shift+Cmd+X strikethrough) — all OO combos matched exactly.
- **Verification:** editor suite 126/126 (3 agent tests had over-strict
"exactly one x"/whole-line pins broken by parallel merges — narrowed pins to
the owning block/line, `24df0680d`); shortcuts-gate PASS; census-shortcuts
**missing 0** (was 6); census-ctx **missing 0** (was 13). Deployed
prod+staging (editor.js/i18n.js/index.html/style.css, md5-verified, live
greps OK), prod+staging **0 pageerrors**.
- **Ledger rebuilt: L0 18 → 0** (501 {L0:0, L1:477, L3:24}; roundtrip 21/21
intact; both ledger.json paths synced). The two vector parks registered in
`interact-divergences.json` + `build.py REGISTERED_PARKS` → divergenced at
build. Loop exited cleanly (batch 23 empty).

## Completed: full OO↔WO parity coverage (L0 = 0, 2026-11-01)

The 501-feature ledger has no L0 gaps: every feature has at least an L1
surface or a declared loud divergence. Straight completion of the remaining
Chromium/Mac-bound shortcut set on future work is bounded by the two
documented vector subsystems (bezier point/contour editing).

## Next queue

- [x] ~~af loop re-arm~~ DONE 2026-11-01: batches 21–22 ran the final 18 L0
      rows (16 real, 2 registered divergences), all merged, loop exited
      cleanly (parked=81, queue empty). Re-arm only if a real new gap row
      appears.

## Notes / traps

- **Auto-reset trap (RESOLVED 2026-10-13):** an every-2h job used to do
  `git reset --hard origin/main` on `server/`; un-pushed commits/changes
  were destroyed (lost `0fb301b97`, recovered + re-pushed). Verified
  2026-10-13: the job no longer runs — uncommitted wo-agent WIP survived
  multiple :58 windows overnight. Historical note only.
- DOCX exporter embeds images via python-docx/PIL: **no SVG**. In-browser SVG
  must be rasterized to PNG (`insertSVGImage`) before insertion.
- i18n `t()` falls back to the raw key — new `data-i18n` keys must be added
  to the catalog in `web/i18n.js` or stripped.

## L2 ACTS behavioral scoring — DONE (2026-11-01, harness `66d998e`)

Follow-up to Phase 5 (user: "option 1" = L2 scoring). New two-pass live
behavior probe `census-wo-acts.cjs` + `build.py` L2 merge.

- Probe: in the prod editor (text doc, then a table-seeded doc, caret in
  cell) it performs a REAL user action per command surface (button click /
  ctx click / wo-command dispatch) and records whether `#editor` mutated
  via a page-side MutationObserver (delta over an ambient settle window).
  Key finding: the prod editor's async WASM model re-sync reverts raw
  execCommand styling within ~150 ms — innerHTML diffing under-counts badly;
  the observer catches even transient mutations (durability is L3's job).
- Dialogs: openers get one primary-action confirm attempt before they count
  as surface-only. Honest noops recorded for context-dependent actions
  (multi-cell merge/split, object-in-cell resize) — those stay L1.
- Results: 209 surfaces, 85 mutated across both passes (text pass 58,
  table pass +27 table ctx ops). Ledger L2 merge links each L1 row's
  wo.match to the probe result and promotes only provably-mutating rows.
- **Ledger 501 → L0 0 · L1 430 · L2 47 · L3 24** (13 acts rows also carry
  roundtrip persistence, deduped by max()). Re-run census-wo-acts.cjs
  before a rebuild whenever the editor surface changes.
