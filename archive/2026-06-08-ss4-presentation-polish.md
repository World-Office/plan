# Sprint SS4: Presentation Polish & Export

**Duration:** 2026-06-08 → 2026-06-12
**Status:** Active
**Dependencies:** SS3 (Animations & Transitions) — Complete
**Based on:** `plan/2026-06-05-ss3-animations-transitions.md` (Task 6 stretch)

## Current State

- **SlidePresenter.tsx** — Component exists (uncommitted), store wired (`isPresenting`, `startPresentation`, `endPresentation`, `nextSlide`, `prevSlide`), keyboard shortcuts (F5/Esc), App.tsx imports. Shows title + placeholder content.
- **CSS** — Two duplicate blocks of presenter styles in `presentation.css` (lines 278–411 and 472–565). Second block is newer/better.
- **PPTX Backend** — Complete (model, parser, serializer, roundtrip tests). No frontend export button.
- **Speaker Notes** — `slide.notes` field exists in store model, SlidePresenter renders notes. No UI to edit them.
- **PPTX Animations** — Not implemented in backend (SS3 Task 6 stretch). Frontend store has animation data, but backend doesn't parse/serialize PPTX animation XML.

## Tasks

### Task 1: Fix Duplicate Presenter CSS
**Files:** `apps/web/apps/presentationeditor-react/src/styles/presentation.css`
**What:** Remove duplicate presenter styles (lines 278–411), keep improved version (lines 472+).
**Acceptance:** No duplicate CSS rules. Presenter overlay renders correctly.

### Task 2: Wire Full Slide Content in SlidePresenter
**Files:**
- `apps/web/apps/presentationeditor-react/src/components/SlidePresenter/SlidePresenter.tsx`
- `apps/web/apps/presentationeditor-react/src/stores/PresentationStore.ts`

**What:**
- Replace "Click to add content" placeholder with actual slide content rendering (shapes, text boxes)
- Use slide data from store (already has shapes with text/position data)
- Render text boxes with correct content and positioning
- Handle blank/title/content layouts visually

**Acceptance:**
- Slides show actual text content (not placeholder)
- Multiple text boxes render in correct positions
- Layout-specific rendering (blank/hides content area)
- Speaker notes panel shows notes content

### Task 3: Speaker Notes Editor
**Files:**
- `apps/web/apps/presentationeditor-react/src/components/RightMenu/` (new or extend)
- `apps/web/apps/presentationeditor-react/src/stores/PresentationStore.ts`

**What:**
- Textarea in slide properties/right panel for editing speaker notes
- Persists to store on change
- JSON save/load roundtrip preserves notes

**Acceptance:**
- Notes textarea in right panel
- Typing updates store
- Notes persist through save/load

### Task 4: PPTX Export Button
**Files:**
- `apps/web/apps/presentationeditor-react/src/components/Toolbar/` (add export button)
- Possibly a download helper function

**What:**
- "Export PPTX" button in toolbar (File or Home tab)
- Serializes current presentation state to JSON
- Sends to conversion-service or generates PPTX via API call
- Downloads resulting .pptx file

**Acceptance:**
- Button visible in toolbar
- Click triggers PPTX generation
- Valid PPTX file downloads

### Task 5 (Stretch): PPTX Animation/Transition OOXML Backend
**Files:**
- `core/crates/wo-ooxml/src/model.rs`
- `core/crates/wo-ooxml/src/parser.rs`
- `core/crates/wo-ooxml/src/serializer.rs`
- `core/crates/wo-ooxml/src/roundtrip.rs`

**What:**
- Add `SlideTransition` model type (transition effect enum: Fade, Push, Wipe, etc.)
- Add `SlideAnimation` model type (animation effect, start trigger, duration, delay)
- Parse `p:transition` from slide XML in parser
- Parse `p:anim` / `p:animEffect` from slide XML
- Serialize transition/animation to slide XML
- Roundtrip test

**Acceptance:**
- Model types defined
- Parse existing PPTX files with transitions
- Serialize roundtrip preserves transition data
- 3+ new tests passing

### Task 6: Verification
- Fix duplicate CSS
- Build slide presenter content rendering
- Verify with pnpm typecheck + build
- Run cargo test for modified crates
