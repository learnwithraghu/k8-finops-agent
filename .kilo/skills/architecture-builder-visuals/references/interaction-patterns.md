# Interaction Patterns — Architecture Builder

## HTML shell (section builders — default)

```html
<div id="toolbar">
  <button class="btn btn-hint" id="btn-hint">Need a hint?</button>
  <button class="btn btn-solve" id="btn-auto-solve">Auto Solve</button>
  ...
</div>
<div id="app">
  <aside id="palette">
    <div class="palette-section">
      <h2>Available</h2>
      <div id="palette-available"></div>
    </div>
    <div class="palette-section">
      <h2>On canvas</h2>
      <div id="palette-placed"></div>
    </div>
    <div class="palette-hint">...</div>
  </aside>
  <div id="canvas-wrap">
    ...
    <div id="hint-callout" aria-live="polite" role="status">
      <div class="hint-title">Hint</div>
      <div class="hint-text" id="hint-text"></div>
    </div>
    <div id="status">...</div>
  </div>
</div>
```

Legacy RAG builder omits `#canvas-viewport`, `#canvas-frame`, and zoom controls — uses scrollable `#canvas-wrap` instead.

---

## Mode A: Template + edit (RAG builder — legacy dark)

**Load state**: pre-wired nodes + edges in `DEFAULT_*_TEMPLATE`.

**Interactions**:
- Drag nodes to reposition; wires re-route via `renderWires()`
- Click output port → input port to add connections
- Select wire + Delete to remove
- Drag from palette to canvas to add optional components
- Reset restores template

**Run Flow**: animate wires in pedagogical sequence (no correctness validation).

Reference: `visual-learning/visuals/rag_architecture_builder/index.html`

---

## Mode B: Placeholder slots (section builders — AWS light)

**Load state**: fixed `SLOT_DEFS` with `filled: null`; fixed `WIRE_DEFS`.

Reference: `sections/01-cluster-foundation/architecture_builder/index.html`

### Slot data shape

Each slot needs `storyHint` — a plain-language domain line (what the slot is *for*, not the component name):

```javascript
const SLOT_DEFS = [
  {
    id: 's8',
    step: 8,
    expected: 'payment',
    storyHint: 'Collecting money service',
    x: 850,
    y: 300,
  },
  // ...
];
```

**Good story hints**: "Runs containers on your laptop", "Collecting money service", "Handles ticket reservations"

**Bad story hints** (answer keys): "Docker", "Container runtime", "payment namespace"

### Empty slot display

```javascript
el.innerHTML = `
  <div class="slot-step">Step ${slot.step}</div>
  <div class="slot-story-hint">${slot.storyHint}</div>`;
```

Do **not** show structural labels like "Foundation · slot 1" or tool names.

### Interactions

- **Available** palette items draggable; drop only onto slots
- Once placed, component leaves **Available** and appears in **On canvas** (with step badge)
- Drag from **On canvas** or filled slot to reassign; drop on filled slot **swaps** components
- Filled slot shows icon + label + × clear button; filled slots are also draggable
- Click × → component returns to **Available**
- Reset clears slots, **re-shuffles Available order**, clears hint tiers, **re-fits view**

### Dual palette — Available / On canvas

Do **not** group into Foundation / Namespaces / Distractors (that reveals answers).

```javascript
let availableOrder = []; // shuffled on load + Reset

function getPlacedTypes() {
  return new Set(slots.filter(s => s.filled).map(s => s.filled));
}

function renderAvailable() {
  // palette-available: COMPONENTS keys not in getPlacedTypes(), order from availableOrder
}

function renderPlaced() {
  // palette-placed: slots.filter(s => s.filled) — draggable with sourceSlotId
}

function renderPalette() {
  renderAvailable();
  renderPlaced();
}
```

Drag payload (both palette and slot sources):

```javascript
const DRAG_MIME = 'application/x-builder';
// { type, sourceSlotId: null | 's3' }
```

`assignComponentToSlot(slot, payload)` handles move/swap from slot or fresh place from Available.

Call `renderPalette()` inside `renderAll()`. Include 3–5 plausible distractors in COMPONENTS (only correct types appear in slots once placed).

### Progressive hint callout

Toolbar **Need a hint?** shows a floating `#hint-callout` (inside `#canvas-wrap`, **not** in the palette) with tiered client-side hints (no LLM).

```javascript
const HINT_TIERS = {
  s1: [
    'Tier 0 — connect story hint to section narrative',
    'Tier 1 — domain category nudge',
    'Tier 2 — strong nudge without literal label',
  ],
};

function getNextHint() {
  // 1. First wrong fill (lowest step) → shortened VALIDATION_MESSAGES nudge
  // 2. Else first empty slot → HINT_TIERS[slotId][tier]; advance tier on repeat
  // 3. Else all filled → "Press Run Flow to validate"
}

function showHint() {
  // positionHintCallout(slotId) — anchor below/above target slot via getBoundingClientRect
  // focusSlotInView(slotId) — pan canvas so slot is visible
  // scheduleHintFade() — auto-dismiss after 10s
}
```

Track `hintTiersUsed`, `lastHintSlotId`, and `hintFadeTimer`; clear all on Reset. Brief `.warning` flash on hinted slot.

### Auto Solve

Toolbar **Auto Solve** fills only slots where `filled !== expected` (empty or wrong), leaves correct placements untouched, then calls `runValidation()`.

```javascript
function getSlotsInValidationOrder() {
  if (typeof VALIDATION_GROUPS !== 'undefined') {
    return VALIDATION_GROUPS.flatMap(g => g.slots.map(getSlot)).filter(Boolean);
  }
  return slots.slice().sort((a, b) => a.step - b.step);
}

async function autoSolve() {
  // 1. For each slot in validation order where filled !== expected:
  //    resolveAutoPlaceConflicts → animatePlacementGhost → assign expected
  // 2. await runValidation() — wire pulses + success message
}
```

- `.placement-ghost` — fixed-position chip animating from palette to slot (~450ms)
- Guard with `isRunning` (same as drag/pan/hint during Run Flow)
- Reset removes any leftover ghosts and hides hint callout

### Palette — shuffled single list (legacy note)

Older builders used one `#palette-components` list that never removed placed items. **New builders** use Available / On canvas instead.

### Pan and zoom

Required for section builders with wide slot layouts.

```javascript
const viewState = { x: 0, y: 0, scale: 1 };
const MIN_SCALE = 0.5;
const MAX_SCALE = 1.5;

function applyViewTransform() {
  canvasEl.style.transform = `translate(${viewState.x}px, ${viewState.y}px) scale(${viewState.scale})`;
}

function fitDiagramToView() {
  // bounding box from SLOT_DEFS positions + padding
  // center and scale to fit #canvas-viewport
}
```

- **Pan**: pointer-down on `#canvas` background (not `.slot`) + drag
- **Zoom**: wheel on viewport; −/+ buttons; Fit and Center buttons
- **Auto-fit**: on load, Reset, and `window.resize`
- **Guard**: disable pan/zoom while `isRunning` (Run Flow active)

### Run Flow validation

Validate sequentially; stop on first empty or wrong component.

```javascript
for (const slot of slots) {
  if (!slot.filled) {
    setStatus(`Step ${slot.step} is empty — "${slot.storyHint}" still needs a component`, 'error');
    return;
  }
  if (slot.filled !== slot.expected) {
    setStatus(getValidationMessage(slot, slot.filled), 'error');
    return;
  }
  await animateWireIntoSlot(slot);
  flash success on slot;
}
setStatus('Complete message → next section', 'success');
```

**VALIDATION_MESSAGES**: `{ [slotId]: { [wrongType]: string, default: string } }` — detailed teaching copy per wrong pick. Story hints stay short; validation messages teach *why*.

---

## Wire routing

**Horizontal chain**: out-right of source → in-left of target.

**Fan-out from hub** (e.g. cluster → namespaces): out-bottom of hub → in-top of child.

```javascript
function bezierPath(x1, y1, x2, y2) {
  const dx = Math.abs(x2 - x1) * 0.55;
  const cx1 = x1 + (x2 >= x1 ? dx : -dx);
  const cx2 = x2 - (x2 >= x1 ? dx : -dx);
  return `M ${x1} ${y1} C ${cx1} ${y1}, ${cx2} ${y2}, ${x2} ${y2}`;
}
```

Each wire group in SVG:
1. `.wire-visible` — static stroke
2. `.wire-pulse` — dash animation overlay
3. `.wire-particle` — circle traveling along path

---

## Copy patterns (toolbar / palette / status)

Section builders use recall-challenge framing:

| Element | Example |
|---------|---------|
| Subtitle | "Recall the foundation chain from the demos — then Run Flow" |
| Palette hint | "Placed components move to **On canvas**. Drag them to reassign slots." |
| Hint button | "Need a hint?" → progressive tiers in floating `#hint-callout` near target slot |
| Auto Solve | Fills wrong/empty slots with fly animation, then runs validation |
| Initial status | "Drag components onto the slots — order matters" |

Row labels on canvas (e.g. "Foundation chain", "Airline namespaces") teach diagram structure only — not answers.

---

## Component data for a new section builder

When scoping a new builder, define:

1. **SLOT_DEFS** — positions, `expected` type, **`storyHint`** per slot
2. **WIRE_DEFS** — fixed topology
3. **COMPONENTS** — palette entries (correct + distractors); no `group` field needed
4. **VALIDATION_MESSAGES** — teaching strings per slot and wrong type
5. **HINT_TIERS** — 3 progressive hint strings per slot id
6. **ZONE_DEFS** + **VALIDATION_GROUPS** for multi-zone layouts (Sections 02–07)
7. Pan/zoom + shuffle + dual-palette helpers (copy from Section 01 builder)

### Section builder inventory (layout archetypes)

Each section uses a **distinct canvas archetype** matched to its `section_goal.md` — not the same horizontal step chain.

| Section | Archetype | Run button | Key visual |
|---------|-----------|------------|------------|
| 01 | `timeline` | Run Flow | Foundation chain + namespace fan-out |
| 02 | `stack` | Deploy & Inspect | Deploy gate + namespace box with K8 resources |
| 03 | `audit` | Run Audit | Green baseline column vs red problems column |
| 04 | `bridge` | Run Scan | Laptop zone ↔ Kind cluster zone |
| 05 | `layers` | Test Gateway | Vertical infra stack + curl proof rail |
| 06 | `hub` | Collect Snapshot | Agent hub + MCP spokes → JSON sink |
| 07 | `transform` | Run Analysis | Messy input → LLM engine → structured panels |

Link from each section's final guide with a **Try it** block pointing at `architecture_builder/index.html`.

---

## Zone frames

Tinted dashed regions teach diagram structure without revealing answers:

```javascript
const ZONE_DEFS = [
  { id: 'ns', label: 'Inside the namespace', x: 60, y: 115, w: 920, h: 300, tint: 'amber' },
  // tint: amber | green | red | blue
];
```

Render in `#zones-layer` (z-index 0, behind wires/slots) via `renderZones()` inside `renderAll()`.

---

## Grouped validation

When a section has multiple logical zones, validate by group — not one global step order:

```javascript
const LAYOUT = { mode: 'audit', runLabel: '▶ Run Audit', successMsg: '...' };

const VALIDATION_GROUPS = [
  { id: 'lens', label: 'Inspection lens', slots: ['s1', 's2'] },
  { id: 'problems', label: 'Problems', slots: ['s4', 's5', 's6', 's7', 's8'] },
];
```

`runValidation()` loops groups, then slots within each group. Slots may use `zoneTag` instead of "Step N".

---

## Wire routing variants

| Variant | Use | Connection points |
|---------|-----|-------------------|
| `horizontal` | Timeline chains | out-right → in-left |
| `vertical` | Layer stacks (S05) | bottom → top |
| `fanOut` | Hub/spoke (S06) | hub bottom → spoke top |
| `bridge` | Cross-zone (S04) | out-right ↔ in-left across zones |
| `mergeIn` | Spokes → sink (S06) | spoke bottom → wide sink top |
| `dashed` | Feedback loops | `dashed: true` on WIRE_DEFS entry |

---

## Drag-and-drop on slots

```javascript
slotEl.addEventListener('drop', e => {
  e.preventDefault();
  const payload = getDragPayload(e); // { type, sourceSlotId }
  assignComponentToSlot(slot, payload);
  renderAll();
});
```

Palette / placed items / filled slots: `draggable=true` + `setDragPayload(e, type, sourceSlotId)`.

---

## Hosting

```bash
open sections/NN-section/architecture_builder/index.html
```

No server required. Works on GitHub Pages as a static file.
