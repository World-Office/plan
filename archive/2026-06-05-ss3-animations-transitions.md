# Sprint SS3: Animations & Transitions

**Duration:** 2026-06-05 → 2026-06-11
**Status:** Planned
**Dependencies:** None (store has `animationEffect`, `transitionEffect`, etc.)

## Goal

Wire up the existing AnimationTab and TransitionsTab UI stubs, implement animation pane, add preview playback, persist to JSON/PPTX.

## Current State

- **AnimationTab.tsx** — Full UI layout with buttons for: animation type (None/Entrance/Emphasis/Exit/Motion Paths), Preview, Animation Pane, Start timing (On Click/With Previous/After Previous), Duration (Fast/Normal/Slow/Very Slow), Delay (0s/0.25s/0.5s/1s), Reorder (Move Earlier/Later) — all handlers are `() => {}`
- **TransitionsTab.tsx** — Full UI layout with: effect buttons (None/Fade/Push/Wipe/Split/Reveal/Checker/Zoom/Morph/Circle/Uncover/Cover), Duration (5 levels), Sound toggle, Advance Slide (On Mouse Click/After with timing), Apply to All — all handlers are `() => {}`
- **PresentationStore** — Has: `transitionEffect: TransitionEffect`, `transitionDuration: number`, `transitionSoundEnabled: boolean`, `animationEffect: AnimationEffect`, `animationStart: StartAnimation` — with corresponding `set*` actions. Serialization in `toJSON`/`fromJSON`. Stores single global values, no per-slide data.
- **Slide Thumbnails** — `SlideThumbnails.tsx` has no transition indicator badge.
- **No animation pane** — no component yet for listing/managing animations on a slide.
- **RightMenu** — Has `"animation"` in `RightMenuPanel` type but no AnimationPanel component.

## Tasks

### Task 1: Wire up TransitionsTab (frontend only, no backend)

**Files:**
- `apps/web/apps/presentationeditor-react/src/components/Toolbar/TransitionsTab.tsx`
- `apps/web/apps/presentationeditor-react/src/stores/PresentationStore.ts` (minor addition: `setTransitionEffectPerSlide`)

**What:**
- Connect all effect buttons → `setTransitionEffect(effect)`
- Connect duration buttons → `setTransitionDuration(s)`
- Connect sound toggle → `setTransitionSoundEnabled(bool)`
- Connect advance slide buttons → store actions
- Add `setTransitionAdvanceMode` and `setTransitionAdvanceTiming` store actions
- Add active class highlighting on selected button
- Implement "Apply to All" → applies current transition to every slide
- Persist to JSON (per-slide transition data)

**Acceptance:**
- Clicking a transition effect highlights it and updates store
- Duration/sound/advance buttons affect store state
- Switching slides preserves per-slide transition
- Apply to All sets transition on all slides
- `toJSON`/`fromJSON` roundtrips per-slide transitions

### Task 2: Wire up AnimationTab (frontend only, no backend)

**Files:**
- `apps/web/apps/presentationeditor-react/src/components/Toolbar/AnimationTab.tsx`
- `apps/web/apps/presentationeditor-react/src/stores/PresentationStore.ts` (add per-element animation data)

**What:**
- Connect type buttons (Entrance/Emphasis/Exit/Motion) → `setAnimationEffect(effect)`
- Connect Start timing → `setAnimationStart(start)`
- Connect Duration/Delay → store properties
- Wire Reorder buttons (Move Earlier/Move Later) — operates on animation list for current slide
- Add active class highlighting on selected button
- Store: add `slideAnimations: Map<slideId, AnimationData[]>` for per-slide, per-element animations
- Persist to JSON

**Data model:**
```ts
interface AnimationData {
  id: string
  effect: AnimationEffect
  start: StartAnimation
  duration: number // seconds
  delay: number   // seconds
  elementRef?: string // CSS selector or element ID
  category: "entrance" | "emphasis" | "exit" | "motionPath"
}
```

**Acceptance:**
- Clicking animation type highlights it and sets effect
- Start timing buttons affect store
- Duration/Delay work
- Selecting animation on a slide adds it to animation list
- Inline `AnimationData` type defined in store/types
- JSON roundtrip preserves animation data

### Task 3: Animation Pane

**Files:**
- NEW: `apps/web/apps/presentationeditor-react/src/components/RightMenu/AnimationPanel.tsx`
- `apps/web/apps/presentationeditor-react/src/components/RightMenu/RightMenu.tsx`
- `apps/web/apps/presentationeditor-react/src/styles/rightmenu.css`

**What:**
- Panel listing all animations on current slide
- Each row shows: effect name, start trigger, duration, delay
- Reorder buttons (Move Earlier/Move Later)
- Delete button per animation
- "Add Animation" button (opens animation picker)
- Highlight currently selected animation in AnimationTab

**Acceptance:**
- Opens via RightMenu "animations" panel or AnimationTab "Animation Pane" button
- Lists all animations on current slide
- Reorder works and updates store
- Delete works
- Empty state shows "No animations" message
- Styled consistently with other right menu panels

### Task 4: Preview Playback

**Files:**
- NEW or extend: `apps/web/apps/presentationeditor-react/src/components/SlideCanvas/AnimationPreview.tsx`
- `apps/web/apps/presentationeditor-react/src/components/Toolbar/AnimationTab.tsx` (wire Preview button)

**What:**
- Preview button plays back animations on current slide
- CSS-based animation for common effects (fade, zoom, flyIn, appear)
- Click to advance through sequenced animations
- Stop/Esc to cancel preview
- Transition preview: animate slide transition when selecting effect in TransitionsTab

**Acceptance:**
- Preview button triggers animation sequence on slide elements
- Fade/zoom/flyIn/appear effects render correctly
- Sequenced animations play in order (onClick advances)
- Esc stops preview
- Transition preview shows brief sample animation

### Task 5: Transition Indicator in Slide Thumbnails

**Files:**
- `apps/web/apps/presentationeditor-react/src/components/SlideThumbnails/SlideThumbnails.tsx`
- `apps/web/apps/presentationeditor-react/src/styles/thumbnails.css`

**What:**
- Small badge/icon on slide thumbnail indicating it has a transition effect
- Current effect name shown on hover (title attribute)
- Active transition effect previewed briefly when clicking thumbnail

**Acceptance:**
- Thumbnails show transition badge
- Hover shows effect name
- Visual feedback when transition is applied

### Task 6 (Stretch): PPTX Animation/Transition Model

**Files:**
- `core/crates/wo-ooxml/src/model.rs`
- `core/crates/wo-ooxml/src/parser.rs`
- `core/crates/wo-ooxml/src/serializer.rs`
- `core/crates/wo-ooxml/src/roundtrip.rs`

**What:**
- Add `SlideTransition` model type (transition effect enum, duration, advance mode/timing)
- Add `SlideAnimation` model type (animation effect, start trigger, duration, delay)
- Parse `p:transition` from slide XML in parser
- Parse `p:anim` / `p:animEffect` from slide XML
- Serialize transition/animation to slide XML
- Roundtrip test

**Acceptance:**
- Model types defined matching OOXML schema
- Parse existing PPTX files with transitions
- Serialize roundtrip preserves transition data
- 3+ new tests passing

## Ordering

1. Task 1 (Transitions wiring) — quick win, immediate visual feedback
2. Task 5 (Thumbnail indicators) — depends on Task 1, shows transition state
3. Task 2 (Animation wiring) — larger, needs data model
4. Task 3 (Animation Pane) — depends on Task 2 animation data
5. Task 4 (Preview playback) — depends on Tasks 1-3
6. Task 6 (PPTX backend) — stretch, independent

## Risk

- Animation preview quality will be CSS-only, not true OOXML rendering — acceptable for MVP
- Per-slide data model change may break existing JSON save files — version check in fromJSON
- Task 6 may reveal OOXML complexity (animation schema is large) — defer if >2 days
