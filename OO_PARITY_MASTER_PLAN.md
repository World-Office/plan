# OO→WO Parity Master Plan — "work all the files, miss nothing"

> **Owner:** OO→WO parity program · **Updated:** 2026-10-28
> **Goal:** systematically close every missing feature discovered by the OO
> source-code analysis, driving code work through **agentflow (af)** campaigns
> where the work is parallelizable, with WO census/ledger gates as acceptance.
> Single source of truth for the backlog so no file/layer is dropped.

**Ground truth for gaps:** `wo-test-harness/census/ledger/SOURCE-ANALYSIS.md`
(dialog layer, shortcuts, scenario context menus, asc_* engine surface,
autocorrect, equations/math). Ledger schema: `ledger.json` → `features[]` with
`cluster/feature/kind/level(L0-L4)/oo/wo/evidence`. Scores today: **L0:8,
L1:211, L3:20** (L2/L4 unsupported — a workstream below).

---

## 0. The completeness check — how we "don't miss anything"

Every workstream below is sourced from a specific OO artifact. Before marking
the program done, verify there is **no OO surface with zero WO counterpart**:

- [ ] **Dialog registry:** all `DE.Views.*.textTitle|textWindowTitle` (38) →
      WO `DIALOG_IDS` (41) join complete (no unmatched OO dialog).
- [ ] **Shortcuts:** all 147 `c_oAscDocumentShortcutType` entries judged
      needed-or-diverged.
- [ ] **asc_* engine API (283):** every feature-group mapped to WO or a
      registered divergence row in the ledger.
- [ ] **Ribbon/backstage/statusbar/menus/ctx-menus:** already census-covered;
      extend ctx to scenario-aware (chart/image/shape/table/list/field).
- [ ] **Panel/template set (23 `*.template`):** no panel with zero WO surface.
- [ ] **Autocorrect / equations / forms / signing:** covered by workstreams
      below (no orphaned OO feature area).

---

## Phase 1 — Measurement foundation (unblocks everything) · NOT af

These are **harness/ledger work**, done by us (not parallelizable, must precede
the campaigns that depend on their gates).

### T-001 · WO dialog census + ledger dialog join
- New `census-wo-dialogs.cjs` (mirror of oo-dialogs.cjs against WO): enumerate
  all 41 `DIALOG_IDS`+ root dialogs, capture a snapshot per dialog.
- Extend `ledger/build.py` to join OO dialogs (38) × WO dialogs (41) into a
  dialog cluster; **retires 2 false L0s** (`references.dlg-bookmarks`,
  `plugins.plugin-manager`) → L0:8 → 6.
- Gate: ledger re-score, OO dialogs all matched-or-diverged.

### T-002 · Agricultural context-menu scenario census
- Extend ctx census to walk multiple right-click targets: chart / image /
  shape / table / list / field. Produce scenario-aware ctx rows for BOTH OO
  and WO (P2.2 material: axes, error bars, trendlines, crop, edit-points,
  arrange, distribute, save-as-picture, start-numbering, join/separate,
  insert-several).
- Gate: ledger gets new ctx-<scenario> features.

### T-003 · Shortcut census gate
- `census-shortcuts.cjs`: static-parse OO `Shortcuts.js`/locale (147 types) and
  WO keydown handlers; emit a shortcut ledger cluster with
  match/needed/diverged verdicts.
- Gate: ledger includes a shortcuts cluster; every OO shortcut judged.

### T-004 · L2/L4 instrumentation (long-term)
- Design an L2 (acts) probe harness + L4 (fidelity) scoring for sheet/slide.
- **Deferred** until P3 content features stabilize — put on roadmap, not in
  this campaign set.

**Exit:** ledger re-score honest vs live prod; T-001..T-003 gates green.

---

## Phase 2 — af campaigns (parallelizable code work)

Each campaign = one `config/<campagne>/tasks.json`. All gates are
path-safe, committed-file-only, and use the WO test suite + ledger.

> **af policy from skill:** repos.json must map task→wo-test-harness or server
> repo; `TF_STATE_DIR`/`TF_REPO_DIR` absolute; mkdir state dir first; launch via
> a PID-scrip; base branch clean; NO `pkill -f`. Never SELFTUNE budget; kill
> stalled worker by pid.

### C1 · Shortcuts cluster (biggest single surface)
OO has **147 shortcut types**; WO has ~8 custom + browser-native B/I/U/Z.
- **C1-1** Core editing: alignment (Ctrl+L/E/R/J), bullets/numbers
  (Ctrl+Shift+L), font-size ± (Ctrl+Shift+>/<), sub/sup (Ctrl+=,
  Ctrl+Shift+=), format painter, remove format (Ctrl+Space).
- **C1-2** Insert/nav: page/column break (Ctrl+Enter), non-breaking space
  (Ctrl+Shift+Space), non-breaking hyphen, ©/®/™/€, insert page number,
  insert date.
- **C1-3** App-level: save (have), print (Ctrl+P), undo/redo (native),
  find/replace (have F/H), spellcheck (F7 → open spell dialog),
  update-fields (F9), TOC update, zoom.
- Gate per task: new `shortcuts-<n>.test.mjs` asserting the handler (press key,
  assert command/`data-cmd` fired / DOM effect).

### C2 · List vertical (one campaign: UI + engine + converter)
Closes the numbered/bulleted list depth.
- **C2-1** Context ops: start-numbering-from (NumberingValueDialog), join /
  separate list, continue-numbering (have), restart numbering.
- **C2-2** Dialogs: `ListIndentsDialog`, `EditListItemDialog`,
  `ListSettingsDialog` (multilevel editor).
- **C2-3** **Converter:** emit `w:startValue` + `ilvl` nesting in wo-ooxml
  serializer & parse back in wo-html/wo-ooxml (closes the "list start value"
  vertical gap — UI + `<start>` both).
- Gate per task: WO dialog opens; roundtrip `start`/`ilvl` survives
  (add to roundtrip.cjs); ledger list rows hit L3.

### C3 · Chart advanced suite
OO chart ext/right-panel ops vs WO chart-dialog (type+data only).
- **C3-1** Axes (primary/secondary), axis titles, major/minor gridlines,
  chart title, legend position.
- **C3-2** Error bars, **trendlines** (linear/exponential/MA/std-dev), up/down
  bars, data labels.
- Gate: `chart-advanced.test.mjs` (assert chart canvas renders each added
  element from a fixture dataset).

### C4 · Advanced settings trio (right-panel deep)
- **C4-1** `ParagraphSettingsAdvanced` (indents/spacing/line-break/borders).
- **C4-2** `TableSettingsAdvanced` (borders/margins/position/repeat-header).
- **C4-3** `ImageSettingsAdvanced` (size/position/wrapping/border; WO has
  image-dialog insert + image-alt-dialog only).
- Gate: right-panel advance-links open dialogs; inputs roundtrip into the doc
  HTML/op stream (assert serialized attr).

### C5 · Table ops
- **C5-1** `CellsAddDialog` ("Insert N rows/cols") + `CellsRemoveDialog`.
- **C5-2** Table↔text convert (`TableToTextDialog`, `TextToTableDialog`).
- **C5-3** `TableFormulaDialog` (formula in cell).
- Gate: row/col count assert; convert commands produce/consume text table.

### C6 · Content-control types
OO cc API = plain/rich **+ checkbox + date-picker + list + picture**; WO
cc-dialog = plain/rich/dropdown marker spans only.
- **C6-1** checkbox + dropdown-list controls.
- **C6-2** date-picker + picture controls.
- Gate: `cc-types.test.mjs` (insert each type, roundtrip, persist).

### C7 · Autocorrect (OO option set)
OO `AscAutoCorrectDialog` options: smart quotes, hyphens→dash, first-letter
sentences/cells, double-space period, hyperlink-detection, replace-as-you-type
table, bulleted/numbered auto lists, exceptions.
- Start with the `asc_*` set that has engine backing:
  `SmartQuotes, HyphensWithDash, FirstLetterOfSentences, FirstLetterOfCells,
  DoubleSpaceWithPeriod, Hyperlinks, AutomaticBulletedLists,
  AutomaticNumberedLists` + replace-table.
- Gate: `autocorrect.test.mjs` (typing fixture → assert replacement/marking;
  options dialog checkboxes persist).

### C8 · Equations / math (OO `Math.js` + asc_Math*)
- **C8-1** Equation dialog + LaTeX/MML insert (WO has equation-dialog stub?).
- **C8-2** `asc_ConvertEquationToMath` / display-mode; math props.
- Gate: equation fixture roundtrips; math renders in canvas.
  *(Note: verify WO equation state first — editor.js shows equation-dialog in
  DIALOG_IDS.)*

### C9 · Forms mode suite (whole OO area)
OO forms: `FormSettings, FillingStatusSettings, RolesManagerDlg, RoleDeleteDlg,
SaveFormDlg, SendForSigningSettings`. **This is an epic — likely own multi-camp.**
- **C9-1** Form settings + filling status (view-mode toggle).
- **C9-2** Roles manager (recipient roles), save-as-form, send-for-signing.
- Gate: end-to-end form fill → submit → recipient role roundtrip.
  *Recommend: split C9 into its own campaign with 4-6 tasks.*

### C10 · Standalone small features
- **C10-1** `DateTimeDialog` (format + "update automatically") — WO has insert
  current date only.
- **C10-2** Caption dialog (label + chapter numbering config) — WO has
  `insertCaption` command only.
- **C10-3** `StyleTitleDialog` (rename style).
- **C10-4** Text direction (`btnTextDir`, asc_TextDirection; also a converter
  `textDirection` ceiling from ROADMAP P1).
- **C10-5** Table-styles gallery (`generateTableStylesPreviews`).
- Gate: dialog opens; setting roundtrips; ledger row → L3.

### C11 · Signatures
OO signature suite: `addSignatureLine, SetSignatureProps, RemoveSignature(s),
request signatures, goto`. WO: 0 hits.
- **C11-1** Insert signature line + signing dialog.
- Gate: signature line inserted + roundtrips in document.

### C12 · Macros (epic — own campaign or deferred)
OO has full macro dialog (Run/Debug/Copy/Rename/Delete + autostart). **WO has
honest event-marker stubs** ("no macro engine exists yet", editor.js:5131).
- This is a **major engine build, not a parity fix**. **Defer** to a dedicated
  project (roadmap P5 ecosystem). Park as ledger divergence row, don't af it.

### C13 · Scenarios beyond word
- **C13-1** sheet/slide/PDF/Visio census (multi-app parity) — new apps in
  WO are separate trees; park as roadmap P2 measurement, not editor code.
- **C13-2** Capability-plane (chat/suggest/live-viewer/forms-fill server
  features) — platform scope; register as divergence rows.

---

## Phase 3 — Integration & honest re-score

- **T-005** Fold everything back into the ledger: re-run WO census against
  live prod (`WO_URL=http://192.168.42.42:8082/word/`), rebuild ledger,
  re-score L0/L1/L3.
- **T-006** Roundtrip 13/13 must still hold (add new fixtures for list-start,
  cc-types, text-direction, equations as they land).
- **T-007** Prod deploy + pageerror sweep + roundtrip probe (standing rule).
- **T-008** Register officially-diverged features (forms-as-own-epic, macros,
  capability plane) as `divergence:` rows so they stop re-surfacing as gaps.

---

## Execution order & which need af

| Step | Work | via af? | Depends | Gate |
|---|---|---|---|---|
| T-001 | WO dialog census + ledger join | no | — | dialogs all matched |
| T-002 | ctx scenario census | no | — | ctx rows added |
| T-003 | shortcut census | no | — | shortcuts cluster |
| C1 | Shortcuts (C1-1/2/3) | **yes, parallel** | T-003 gate | shortcuts tests |
| C2 | List vertical | **yes** (C2-1/2/3 sequential within) | T-001 | roundtrip start/ilvl |
| C3 | Chart advanced | **yes** | T-002 | chart-advanced tests |
| C4 | Adv settings trio | **yes** (3 parallel) | T-001 | panel+roundtrip |
| C5 | Table ops | **yes** | T-001 | row/col+convert |
| C6 | cc types | **yes** | T-001 | cc-types tests |
| C7 | Autocorrect | **yes** | T-001 | autocorrect tests |
| C8 | Equations/math | **yes** | T-001 + verify WO state | equation roundtrip |
| C9 | Forms suite (epic) | **yes**, own campaign | T-001 | form fill e2e |
| C10 | Standalone small | **yes**, batch | T-001 | dialog+roundtrip |
| C11 | Signatures | **yes** | T-001 | signature roundtrip |
| C12 | Macros | **defer** (own project) | — | divergence row |
| C13 | Multi-app/capability | **park** | — | divergence rows |
| T-005..8 | integrate + re-score + deploy | no | all above | ledger honest, 13/13, prod clean |

**Loose deps:** C2-3 (converter) must reflect into roundtrip gate before C2
closes. C9,C12 are epics; keep OUT of the mixed batch campaigns so a failure
doesn't DAG-block the rest. Mixed carve-up: **C1+C3+C4+C7+C10** in the first
launch wave (independent, high count); **C2+C5+C6+C8+C11** second; **C9** third
alone; C12/C13 documented divergences.

---

## Tooling invariants (from operating memory)

- Census runs `/usr/bin/python3` + `/usr/bin/node` (never bare python/node).
- NO_PROXY=127.0.0.1,localhost for local probes. Kill by pid from `ss -tlnp`;
  never `pkill -f` (exit-143 self-match), never kill unrelated buildx
  (chemie-hugo ~pi3116195).
- Deploy = cp index.html editor.js i18n.js style.css → `~/editor-ui-ebae8fc3/word/`;
  landed JS `node --check`; i18n keys in BOTH en + de.
- Matcher aliases live in `build.py` (never patch JSONs); `want` targets
  `norm()`ed before compare.
- NEW fixtures must roundtrip verbatim (identity sanitize) so regressions fail.
- af: base branch clean; path-safe committed gates; NO CHANGE ≠ SUCCESS
  (empty-diff tasks fail).

---

## Definition of done (program-level)

1. Phases 1–3 executed; every OO surface in the "completeness check" (§0) is
   matched-or-diverged in the ledger.
2. Ledger re-scored honest vs live prod: **L0 ≤ 6** (down from 8, after
   T-001 retires 2 false rows) **and every real gap has a task**; new
   L3 rows for list-start, cc-types, text-direction, equations, signatures,
   autokorrect as they land.
3. Roundtrip 13/13 + extended fixtures green; prod pageerror sweep 0.
4. Divergence rows (forms-mvp, macros, capability-plane, multi-app) registered
   so they stop re-appearing as unresolved gaps.
5. `plan/PARITY_GAPS.md` superscripted pointing at this plan + SOURCE-ANALYSIS.
