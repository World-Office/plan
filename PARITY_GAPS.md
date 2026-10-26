> ⚠️ **SUPERSEDED 2026-10-26** by the OO→WO deep census (wo-test-harness/census):
> parity arc closed at OO 269 vs WO 272 rows, deficit 3 (all three structurally
> not-controls). The asc-gen control clusters below belong to the pre-arc census
> methodology and are resolved by the honest-matcher gap report. The one "known
> gap" (ParagraphSettings dialog) is covered by the right panel (AF7/AF15).
> Historical reference only — do not use as a backlog.

# Word-Office Parity Gaps

Generated 2026-10-13 from word-parity-contracts.json (361 entries, census-oo walk).

This report is the explicit replacement for the implicit "covered" balance: every OO control that WO does NOT fully mirror appears here with tab, control, and what exactly is missing.

## Known gaps with failing contract (1)

- **paragraph-line-spacing** (home/dialog) — KNOWN GAP: OO's line-spacing entry leads to a ParagraphSettings dialog (alignment/indent/spacing/widow control). WO only has a line-height select — no dialog exists. Full OO ParagraphSettings lives in the right panel, which the census walk does not capture.
  - missing sub-feature: spacing before/after numeric (`[name=spacing-before]`)
  - missing sub-feature: first-line indent (`[name=first-line]`)
  - missing sub-feature: widow/orphan control (`[name=widow]`)

## Stubs (0)

none — every shipped control has a real contract target.

## Unverified — contract red (0)

none — all executed contracts green (gate PASS).

## Covered clusters awaiting sub-feature mapping (152 controls in 14 tabs)

These WO controls map to MULTIPLE OO controls (one WO button absorbs an OO dialog with 10-20 options). Presence is proven; behavior is not contracted per sub-feature yet. Each cluster needs: OO original dialog walked once, active controls recorded as selector list, override subFeatures[] filled.

- **collaboration** (20): copy, paste, cut, addcomment, , delete, resolve, asc-gen509, asc-gen511, accept, reject, asc-gen525, word-count, english-united-states
- **plugins** (16): copy, paste, cut, asc-gen4556, , asc-gen4572, asc-gen4582, asc-gen4584, asc-gen4586, asc-gen4588, asc-gen4590, word-count, english-united-states
- **view** (15): copy, paste, cut, asc-gen896, asc-gen920, asc-gen922, asc-gen935, asc-gen933, interfacetheme, asc-gen926, asc-gen937, asc-gen939, asc-gen941, word-count, english-united-states
- **chart-design** (14): copy, paste, cut, chartelements, asc-gen830, editdata, asc-gen842, chart-type, asc-gen856, wrapping, asc-gen865, word-count, english-united-states, asc-gen844
- **draw** (13): copy, paste, cut, asc-gen670, , asc-gen668, word-count, english-united-states
- **layout** (13): copy, paste, cut, , breaks, wrapping, bringforward, sendbackward, align, word-count, english-united-states
- **insert** (12): copy, paste, cut, blankpage, , breaks, addcomment, insertdatetime, word-count, english-united-states
- **home** (9): copy, paste, cut, text-direction, replace, select-all, word-count, english-united-states, asc-gen476
- **references** (9): copy, paste, cut, , asc-gen893, word-count, english-united-states
- **_global** (8): copystyle, asc-gen989, asc-gen987, status-btn-multiple-pages, btn-zoom-topage, btn-zoom-towidth, btn-zoom-down, btn-zoom-up
- **protection** (7): copy, paste, cut, asc-gen541, asc-gen546, word-count, english-united-states
- **ai** (7): copy, paste, cut, , word-count, english-united-states
- **header-footer** (6): copy, paste, cut, insertdatetime, word-count, english-united-states
- **backstage** (3): return, save, print

## Census walk gaps (surfaces the manifest cannot see)

- **Right-click context menu** — census-oo.cjs walks ribbon tabs + file menu only; OO context-menu controls (cut/copy/paste/font options at cursor) are invisible to the manifest. Extend census-oo.cjs with a contextmenu capture before contracting this surface.
- **OO right panel** — the OO properties panel (paragraph/shape/chart advanced settings) is not part of the ribbon walk; its entry points (e.g. line-spacing options) appear as single ribbon controls.

