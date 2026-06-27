# Interaction Patterns — Architecture Builder

## HTML shell

```html
<div id="toolbar">...</div>
<div id="app">
  <aside id="palette">...</aside>
  <div id="canvas-wrap">
    <div id="canvas">
      <svg id="wire-layer"></svg>
      <div id="nodes-layer"></div>  <!-- or #slots-layer -->
    </div>
    <div id="status">...</div>
  </div>
</div>
<svg id="icon-sprites">...</svg>
<script>...</script>
```

## Mode A: Template + edit (RAG builder)

**Load state**: pre-wired nodes + edges in `DEFAULT_*_TEMPLATE`.

**Interactions**:
- Drag nodes to reposition; wires re-route via `renderWires()`
- Click output port → input port to add connections
- Select wire + Delete to remove
- Drag from palette to canvas to add optional components
- Reset restores template

**Run Flow**: animate wires in pedagogical sequence (no correctness validation).

**Key JS**:
- `bezierPath(x1,y1,x2,y2)` with horizontal control offset
- `portPos(node, 'in'|'out')` for wire endpoints
- `animateParticleAlongPath(pathEl, particleEl, duration)` via `getPointAtLength`

Reference: `visual-learning/visuals/rag_architecture_builder/index.html`

## Mode B: Placeholder slots (Section 01 builder)

**Load state**: fixed `SLOT_DEFS` with `filled: null`; fixed `WIRE_DEFS`.

**Interactions**:
- Palette items draggable; drop only onto slots
- Empty slot shows step number + hint
- Filled slot shows icon + label + × clear button
- Drop on filled slot replaces component
- Reset clears all slots

**Run Flow**: validate sequentially; stop on first empty or wrong component.

**Validation loop** (async):
```javascript
for (const slot of slots) {
  if (!slot.filled) { highlight warning; return; }
  if (slot.filled !== slot.expected) { highlight error; show teaching message; return; }
  await animateWireIntoSlot(slot);
  flash success on slot;
}
setStatus('Complete message → next section', 'success');
```

**VALIDATION_MESSAGES**: map `{ [slotId]: { [wrongType]: string, default: string } }` with teaching copy per distractor.

Reference: `sections/01-cluster-foundation/architecture_builder/index.html`

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

## Palette structure

Group palette items when using distractors:

```html
<div class="palette-section">
  <h2>Foundation</h2>
  <div id="palette-foundation"></div>
</div>
<div class="palette-section">
  <h2>Distractors</h2>
  <div id="palette-distractors"></div>
</div>
```

Component registry:
```javascript
const COMPONENTS = {
  docker: { label: 'Docker', icon: 'icon-docker', group: 'foundation' },
  // ...
};
```

Palette items use `draggable=true` + `dataTransfer.setData('text/plain', type)`.

## Drag-and-drop on slots

```javascript
slotEl.addEventListener('dragover', e => { e.preventDefault(); el.classList.add('drop-target'); });
slotEl.addEventListener('drop', e => {
  e.preventDefault();
  const type = e.dataTransfer.getData('text/plain');
  slot.filled = type;
  renderAll();
});
```

## Component data for a new section builder

When scoping a new builder, define:

1. **SLOT_DEFS** or **DEFAULT_TEMPLATE** — positions + expected types
2. **WIRE_DEFS** — fixed topology
3. **COMPONENTS** — palette entries (correct + distractors)
4. **RUN_SEQUENCE** or validation order
5. **VALIDATION_MESSAGES** — teaching strings (slot mode only)

## Hosting

```bash
open sections/NN-section/architecture_builder/index.html
```

No server required. Works on GitHub Pages as a static file.
