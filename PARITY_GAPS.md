# Word-Office Parity Gaps

Generated 2026-11-07 from word-parity-contracts.json (594 entries, census-oo walk).

This report is the explicit replacement for the implicit "covered" balance: every OO control that WO does NOT fully mirror appears here with tab, control, and what exactly is missing.

## Known gaps with failing contract (1)

- **formatting.paragraph-line-spacing** (?/dialog) — KNOWN GAP: OO's line-spacing entry leads to a ParagraphSettings dialog (alignment/indent/spacing/widow control). WO only has a line-height select — no dialog exists. Full OO ParagraphSettings lives in the right panel, which the census walk does not capture.
  - missing sub-feature: spacing before/after numeric (`[name=spacing-before]`)
  - missing sub-feature: first-line indent (`[name=first-line]`)
  - missing sub-feature: widow/orphan control (`[name=widow]`)

## Stubs (0)

none — every shipped control has a real contract target.

## Unverified — contract red (0)

none — all executed contracts green (gate PASS).

## Covered clusters awaiting sub-feature mapping (0 controls in 0 tabs)

These WO controls map to MULTIPLE OO controls (one WO button absorbs an OO dialog with 10-20 options). Presence is proven; behavior is not contracted per sub-feature yet. Each cluster needs: OO original dialog walked once, active controls recorded as selector list, override subFeatures[] filled.


## Census walk gaps (surfaces the manifest cannot see)

- **Right-click context menu** — census-oo.cjs walks ribbon tabs + file menu only; OO context-menu controls (cut/copy/paste/font options at cursor) are invisible to the manifest. Extend census-oo.cjs with a contextmenu capture before contracting this surface.
- **OO right panel** — the OO properties panel (paragraph/shape/chart advanced settings) is not part of the ribbon walk; its entry points (e.g. line-spacing options) appear as single ribbon controls.

