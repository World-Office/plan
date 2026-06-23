# SS5 Sprint: Editing Core - Undo/Redo + Shape Formatting

**Date:** 2026-06-09
**Previous:** SS4 Presentation Polish & Export (SlidePresenter, notes, PPTX export, animation backend)

## Objective

Add undo/redo support, shape formatting panel, and inline text editing to the presentation editor.

## Key Findings

- PPTX export button exists but backend has no `wo-presentation` → `pptx` converter
- 49/49 wo-ooxml tests pass. Typecheck clean.
- No undo/redo support at all
- Shape properties cannot be edited via UI (only programmatically)
- No inline text editing on canvas

## Tasks

### Task 1: Undo/Redo System
- Create undo/redo history stack in PresentationStore
- Capture slide/shape mutations (addShape, removeShape, moveShape, updateShape, addSlide, etc.)
- Expose undo()/redo() methods
- Ctrl+Z / Ctrl+Shift+Z keyboard shortcuts via useKeyboardShortcuts.ts
- Store: MAX_HISTORY = 50 entries

### Task 2: Shape Properties Panel
- New RightMenu panel: ShapePanel.tsx
- Color picker for fill + stroke
- Stroke width slider
- Text font size, font color editing (for text-containing shapes)
- Rotation angle input
- Position/size inputs (x, y, width, height)
- Delete shape button

### Task 3: Inline Text Editing (stretch)
- Double-click shape in SlideCanvas → enters edit mode
- Text input overlay positioned at shape bounds
- Blur/Escape to save, Enter for newline

### Task 4: Verification
- Typecheck passes
- Manual: shapes can be moved, undo restores position, redo reapplies
- Manual: shape properties panel shows correct values
