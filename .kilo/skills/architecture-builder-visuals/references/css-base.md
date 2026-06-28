# CSS Base — Architecture Builder (AWS Light)

Copy this block at the start of every **section** architecture builder `<style>`. This is the default theme — match [`sections/01-cluster-foundation/architecture_builder/index.html`](../../../../sections/01-cluster-foundation/architecture_builder/index.html).

For the legacy dark RAG builder, copy CSS from `visual-learning/visuals/rag_architecture_builder/index.html` instead.

## `:root` tokens (required)

```css
:root {
  --bg: #F4F6F8;
  --canvas-bg: #FFFFFF;
  --surface: #F8F9FA;
  --surface-hover: #FFF8F0;
  --border: #D5DBDB;
  --border-glow: #FF9900;
  --accent: #FF9900;
  --accent-dark: #EC7211;
  --text: #232F3E;
  --text-muted: #607D8B;
  --wire: #AAB7B8;
  --wire-active: #FF9900;
  --error: #EF5350;
  --warning: #FF9900;
  --success: #34A853;
  --toolbar-h: 56px;
  --palette-w: 210px;
  --slot-w: 150px;
  --slot-h: 84px;
  /* template mode: --node-w: 160px; --node-h: 72px; */
}
```

## Reset + body

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body {
  height: 100%;
  overflow: hidden;
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
}
```

## Toolbar

```css
#toolbar {
  height: var(--toolbar-h);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  background: #FFFFFF;
  border-bottom: 1px solid var(--border);
  z-index: 100;
}

#toolbar h1 {
  font-size: 1.05rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--text);
}
```

## Buttons

```css
.btn {
  padding: 8px 18px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn:hover { background: var(--surface-hover); border-color: var(--border-glow); }

.btn-primary {
  background: linear-gradient(135deg, var(--accent), var(--accent-dark));
  border-color: var(--accent);
  color: #fff;
}

.btn-primary:hover {
  box-shadow: 0 0 16px rgba(255, 153, 0, 0.35);
  transform: translateY(-1px);
}

.btn-primary.running {
  animation: pulse-btn 1s ease infinite;
  pointer-events: none;
  opacity: 0.85;
}

@keyframes pulse-btn {
  0%, 100% { box-shadow: 0 0 8px rgba(255, 153, 0, 0.3); }
  50% { box-shadow: 0 0 20px rgba(255, 153, 0, 0.55); }
}
```

## Layout shell

```css
#app {
  display: flex;
  height: calc(100vh - var(--toolbar-h));
}

#palette {
  width: var(--palette-w);
  flex-shrink: 0;
  background: #FFFFFF;
  border-right: 1px solid var(--border);
  padding: 14px 10px;
  overflow-y: auto;
}

#canvas-wrap {
  flex: 1;
  position: relative;
  overflow: hidden;
  background: #EEF1F3;
}

#canvas-viewport {
  width: 100%;
  height: 100%;
  overflow: hidden;
  cursor: grab;
  touch-action: none;
}

#canvas-viewport.panning { cursor: grabbing; }

#canvas {
  width: 1240px;
  height: 460px;
  position: relative;
  background-color: var(--canvas-bg);
  background-image: radial-gradient(circle, #E8ECED 1px, transparent 1px);
  background-size: 24px 24px;
  transform-origin: 0 0;
  will-change: transform;
}

#canvas-frame {
  position: absolute;
  left: 16px;
  top: 64px;
  width: 1188px;
  height: 330px;
  border-radius: 16px;
  border: 1px solid rgba(255, 153, 0, 0.25);
  background: #FAFAFA;
  box-shadow: inset 0 0 30px rgba(255, 153, 0, 0.04);
  pointer-events: none;
  z-index: 0;
}

.canvas-controls {
  position: absolute;
  bottom: 52px;
  right: 16px;
  display: flex;
  gap: 6px;
  z-index: 12;
}
```

## Palette item

```css
.palette-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px 8px 12px;
  margin-bottom: 5px;
  border-radius: 9px;
  border: 1px solid transparent;
  border-left: 3px solid rgba(255, 153, 0, 0.65);
  background: var(--surface);
  cursor: grab;
  transition: all 0.2s;
  user-select: none;
}

.palette-item:hover {
  border-color: var(--border-glow);
  background: var(--surface-hover);
  box-shadow: 0 0 10px rgba(255, 153, 0, 0.12);
}

.palette-item .icon-wrap {
  width: 26px;
  height: 26px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
}

.palette-hint {
  margin-top: 10px;
  padding: 10px;
  border-radius: 8px;
  background: #FFFBF2;
  border: 1px solid rgba(255, 153, 0, 0.25);
  font-size: 0.68rem;
  color: var(--text-muted);
  line-height: 1.55;
}
```

## Wire animation

```css
.wire-visible {
  fill: none;
  stroke: var(--wire);
  stroke-width: 2;
  transition: stroke 0.2s;
}

.wire-visible.active {
  stroke: var(--wire-active);
  stroke-width: 3;
  filter: drop-shadow(0 0 4px rgba(255, 153, 0, 0.5));
}

.wire-pulse {
  fill: none;
  stroke: var(--accent);
  stroke-width: 4;
  stroke-linecap: round;
  opacity: 0;
  pointer-events: none;
}

.wire-pulse.animating {
  opacity: 1;
  stroke-dasharray: 12 200;
  animation: wire-travel 0.85s linear forwards;
}

@keyframes wire-travel {
  from { stroke-dashoffset: 212; }
  to { stroke-dashoffset: -212; }
}

.wire-particle {
  fill: var(--accent);
  opacity: 0;
  filter: drop-shadow(0 0 4px rgba(255, 153, 0, 0.6));
}

.wire-particle.animating { opacity: 1; }
```

## Filled card (node or slot)

```css
.node, .slot.filled {
  background: linear-gradient(145deg, #FFFFFF 0%, var(--surface) 100%);
  border: 1.5px solid var(--border);
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(35, 47, 62, 0.08), 0 0 10px rgba(255, 153, 0, 0.1);
}

.node .node-icon, .slot-icon {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 153, 0, 0.1);
  border-radius: 7px;
  color: var(--accent);
}
```

## Empty slot + validation states

```css
.slot.empty {
  border: 2px dashed rgba(255, 153, 0, 0.55);
  background: #FFFBF2;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.8);
  animation: slot-pulse 2.5s ease infinite;
}

@keyframes slot-pulse {
  0%, 100% { border-color: rgba(255, 153, 0, 0.4); }
  50% { border-color: rgba(255, 153, 0, 0.75); }
}

.slot-story-hint {
  font-size: 0.64rem;
  color: var(--text-muted);
  font-style: italic;
  padding: 0 8px;
  line-height: 1.35;
}

.slot-step {
  font-size: 0.58rem;
  color: var(--accent);
  opacity: 0.85;
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.slot.drop-target {
  border-color: var(--accent) !important;
  box-shadow: 0 0 18px rgba(255, 153, 0, 0.3);
  transform: scale(1.04);
}

.slot.error {
  border-color: var(--error) !important;
  box-shadow: 0 0 16px rgba(239, 83, 80, 0.35);
  animation: shake 0.45s ease;
}

.slot.warning {
  border-color: var(--warning) !important;
  box-shadow: 0 0 14px rgba(255, 153, 0, 0.3);
}

.slot.success-flash {
  border-color: var(--success) !important;
  box-shadow: 0 0 16px rgba(52, 168, 83, 0.35);
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(-6px); }
  40% { transform: translateX(6px); }
  60% { transform: translateX(-4px); }
  80% { transform: translateX(4px); }
}
```

## Hint callout + Auto Solve buttons

```css
#hint-callout {
  position: fixed;
  z-index: 60;
  max-width: 300px;
  padding: 12px 14px;
  border-radius: 10px;
  background: #F0F7FF;
  border: 1px solid rgba(66, 133, 244, 0.35);
  box-shadow: 0 4px 16px rgba(35, 47, 62, 0.12);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.4s ease;
}

#hint-callout.visible { opacity: 1; }
#hint-callout.fading { opacity: 0; }

.btn-hint {
  border-color: rgba(66, 133, 244, 0.4);
  color: #4285F4;
}

.btn-solve {
  border-color: rgba(52, 168, 83, 0.45);
  color: var(--success);
}

.placement-ghost {
  position: fixed;
  z-index: 1000;
  pointer-events: none;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 8px;
  background: #FFFFFF;
  border: 2px solid var(--success);
  box-shadow: 0 6px 20px rgba(35, 47, 62, 0.18);
  font-size: 0.75rem;
  font-weight: 600;
}
```

## Status bar

```css
#status {
  position: fixed;
  bottom: 14px;
  left: calc(var(--palette-w) + 50%);
  transform: translateX(-50%);
  max-width: 620px;
  padding: 8px 18px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.96);
  border: 1px solid var(--border);
  font-size: 0.76rem;
  color: var(--text-muted);
  z-index: 10;
  text-align: center;
  box-shadow: 0 2px 12px rgba(35, 47, 62, 0.08);
}

#status.active { color: var(--accent); }
#status.error { color: var(--error); border-color: rgba(239, 83, 80, 0.4); }
#status.success { color: var(--success); border-color: rgba(52, 168, 83, 0.4); }

#icon-sprites { display: none; }
```

## Legacy dark tokens (RAG builder only)

Do not use for new section builders. Copy from `visual-learning/visuals/rag_architecture_builder/index.html` if extending that file.

```css
/* Legacy — RAG only */
:root {
  --bg: #0b1329;
  --surface: #111b36;
  --cyan: #38bdf8;
  --wire-active: #38bdf8;
  /* ... */
}
```
