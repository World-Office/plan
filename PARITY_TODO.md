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

## Notes / traps

- **Auto-reset trap:** an every-2h job does `git reset --hard origin/main` on
  `server/`. Any un-pushed commit or working-tree change is destroyed.
  **Always commit+push before the top of the hour (:58).** Lost commit
  `0fb301b97` was recovered and is now merged + re-pushed.
- DOCX exporter embeds images via python-docx/PIL: **no SVG**. In-browser SVG
  must be rasterized to PNG (`insertSVGImage`) before insertion.
- i18n `t()` falls back to the raw key — new `data-i18n` keys must be added
  to the catalog in `web/i18n.js` or stripped.
