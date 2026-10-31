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

## Next (unchanged queue)

- [ ] T-006 roundtrip extension (13/13 +
      extra fixtures) / T-008 divergence rows / next census refresh to re-arm
      the af loop (short-term af pool empty).

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
