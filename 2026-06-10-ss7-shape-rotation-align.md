# SS7 Sprint: Shape Rotation & Alignment (Small Lead)

**Date:** 2026-06-10
**Epic:** Presentation Editor Completion
**Status:** Planned

## Overview

Small leading sprint for the **Presentation Editor Completion** epic. Adds rotation control to shapes (rotation handle on canvas + angle input in Shape Panel) and shape alignment tools (align left/center/right/top/middle/bottom, distribute evenly).

## Tasks

### SS7 Task 1: Shape Rotation — Canvas Handle
- Add `rotate` angle property to Shape type (degrees, default 0)
- Add rotation handle visual on selected shapes (small circle above top-center resize handle)
- Drag rotation handle → update shape.rotate → re-render
- Cursor changes to `grab` on rotation handle

### SS7 Task 2: Shape Rotation — Shape Panel Input
- Add angle input field to ShapePanel (0–360°, step 1°, with reset to 0)
- Label: "Rotation"
- MobX auto-sync on change

### SS7 Task 3: Shape Alignment Tools
- Add alignment toolbar section to HomeTab (or floating toolbar)
- Buttons: Align Left, Center, Right, Top, Middle, Bottom
- Behavior: if 1 shape selected → align to slide; if 2+ selected → align to each other
- Distribute Horizontally / Vertically for 3+ selected shapes

### SS7 Task 4: pushSnapshot Integration
- Add `pushSnapshot()` in rotation change and alignment operations
- Undo/redo support via existing history stack

## Verification
- `pnpm typecheck` passes (19/20, pre-existing export-service.ts excluded)
- Rotation handle visible on selected shapes
- Rotation input updates shape
- Alignment buttons work for single and multi-select

---

# Epic: Presentation Editor Completion

**Goal:** Bring presentation editor to feature parity with basic slide applications (Google Slides, PowerPoint Online basic).

## Sprint Sequence

| Sprint | Scope | Size | Est. | Depends On |
|--------|-------|------|------|------------|
| **SS7** | Shape Rotation & Alignment | Small | 1 session | SS5/SS6 |
| **SS8** | PPTX Full Roundtrip Coverage | Large | 5–8 sessions | SS7 |
| **SS9** | ODP Import/Export | Medium | 3–5 sessions | SS8 |
| **SS10** | Slide Background & Templates | Small | 1 session | SS7 |
| **SS11** | Image/Media Insertion into Slides | Medium | 2 sessions | SS5 |
| **SS12** | Flowchart Editor MVP | Extra-Large | 8–12 sessions | N/A |

## Epic Breakdown

### SS8: PPTX Full Roundtrip Coverage
- Audit current PPTX schema coverage (wo-ooxml)
- Add missing slide-level elements (layoutId, masterId, slide transition properties)
- Add missing shape properties (3D, glow, shadow, reflection)
- Add missing chart types and chart formatting
- Add SmartArt diagram roundtrip
- Roundtrip test suite for all PPTX schema elements

### SS9: ODP Import/Export
- ODP (OpenDocument Presentation) format parser in wo-odf
- Slide structure mapping (ODP ↔ internal representation)
- Shape/table/chart conversion between ODP and PPTX
- Roundtrip test corpus

### SS10: Slide Background & Templates
- Per-slide background color/gradient/image
- Slide template system (reuse layouts from theme)
- Background UI in right-click context menu

### SS11: Image/Media Insertion into Slides
- Image shape type (already exists in canvas, wire up InsertTab)
- File picker → insert image as shape
- Image resize/crop handles
- Video/audio embedding placeholder

### SS12: Flowchart Editor MVP
- Node-based editing surface (separate from slides editor)
- Connection routing between nodes
- SVG export
- Basic shape library (rect, diamond, circle, arrow connectors)
