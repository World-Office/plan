# SS6 Sprint: Inline Text Editing + Clipboard

**Date:** 2026-06-09
**Previous:** SS5 Editing Core (Undo/Redo + Shape Properties Panel)

## State Assessment

- **Undo/Redo** ✅ — Full history, Ctrl+Z/Y, 25 mutation methods snapshotted
- **Shape Properties Panel** ✅ — Fill, stroke, position, font, rotation, Delete
- **SlideCanvas** ✅ — Drag-move, 8-resize-handle, click-select, deselect on canvas
- **Content types** ✅ — 8 shapes + chart (5 types) + table + connector rendering
- **Animations/Transitions** ✅ — Full tabs, animation pane, preview, CSS
- **Presenter view** ✅ — F5 start, keyboard nav, speaker notes, timer
- **Toolbar** ✅ — Home/Insert/Design/Transitions/Animation tabs
- **FileMenu** ✅ — Full menu with 10 panels (SaveAs, Print, Info, etc.)
- **Serialization** ✅ — toJSON/fromJSON with full data model
- **LeftMenu + SlideThumbnails** ✅ — Add/duplicate/delete/navigate slides

## Missing Features (SS6 Scope)

### Task 1: Inline Text Editing (Critical UX)
Currently, shapes with text render `shape.text` as SVG `<text>` or `<span>` — no inline editing on canvas.
The only way to edit text is the ShapePanel textarea.

**Implementation:**
- Add `editingShapeId` state to PresentationStore
- Add `startInlineEdit(shapeId)`, `endInlineEdit()`, `updateInlineText(text)` methods
- In SlideCanvas: double-click handler on shapes → `startInlineEdit`
- Render a contentEditable `<div>` overlay at the shape's position/size when in edit mode
- Blur → saves; Enter → newline (Shift+Enter); Escape → cancels
- ShapePanel textarea stays in sync

**Files:** PresentationStore.ts, SlideCanvas.tsx, ShapePanel.tsx

### Task 2: Copy/Paste (Cut/Copy/Paste)
HomeTab has Cut/Copy/Paste buttons with empty onClick — no clipboard support.

**Implementation:**
- Add `clipboardShape: ShapeData | null` to store
- `copyShape()` / `cutShape()` / `pasteShape()` methods
- `pasteShape()`: duplicate with offset (30px), selects new shape, pushSnapshot
- `cutShape()`: copy + removeShape
- Wire HomeTab buttons to store methods
- Use system clipboard API for cross-app paste if applicable

**Files:** PresentationStore.ts, HomeTab.tsx

### Task 3: New Slide button in InsertTab
InsertTab's "New Slide" button has empty onClick.

**Implementation:**
- Wire to `presentationStore.addSlide()`

**Files:** InsertTab.tsx

## Verification
- pnpm typecheck passes
- Double-click shape → inline text editing works
- Copy/paste shapes duplicates with offset
- Enter for newline, Escape to cancel
- No regressions in undo/redo or shape panel
