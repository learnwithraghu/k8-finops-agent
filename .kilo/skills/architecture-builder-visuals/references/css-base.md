# CSS Base — Architecture Builder

Copy this block at the start of every architecture builder `<style>`. Add mode-specific rules after it.

## `:root` tokens (required)

```css
:root {
  --bg: #0b1329;
  --surface: #111b36;
  --surface-hover: #162040;
  --border: #2a3a60;
  --border-glow: #38bdf8;
  --teal: #028090;
  --teal-bright: #02c39a;
  --cyan: #38bdf8;
  --text: #e2e8f0;
  --text-muted: #94a3b8;
  --wire: #1e4d6b;
  --wire-active: #38bdf8;
  --port: #028090;
  --port-hover: #02c39a;
  --error: #ef5350;
  --warning: #ffb84d;
  --success: #02c39a;
  --toolbar-h: 56px;
  --palette-w: 210px;
  --node-w: 160px;
  --node-h: 72px;
  /* slot mode: --slot-w: 150px; --slot-h: 76px; */
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
  background: linear-gradient(180deg, #0e1830 0%, var(--bg) 100%);
  border-bottom: 1px solid var(--border);
  z-index: 100;
}

#toolbar h1 {
  font-size: 1.05rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  background: linear-gradient(90deg, var(--cyan), var(--teal-bright));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
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
  background: linear-gradient(135deg, var(--teal), #036666);
  border-color: var(--teal-bright);
  color: #fff;
}

.btn-primary:hover {
  box-shadow: 0 0 20px rgba(56, 189, 248, 0.35);
  transform: translateY(-1px);
}

.btn-primary.running {
  animation: pulse-btn 1s ease infinite;
  pointer-events: none;
  opacity: 0.85;
}

@keyframes pulse-btn {
  0%, 100% { box-shadow: 0 0 10px rgba(56, 189, 248, 0.3); }
  50% { box-shadow: 0 0 28px rgba(56, 189, 248, 0.6); }
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
  background: #0c152b;
  border-right: 1px solid var(--border);
  padding: 14px 10px;
  overflow-y: auto;
}

#canvas-wrap { flex: 1; position: relative; overflow: auto; }

#canvas {
  min-width: 1000px;
  min-height: 480px;
  width: 100%;
  height: 100%;
  position: relative;
  background-color: var(--bg);
  background-image: radial-gradient(circle, #1e293b 1px, transparent 1px);
  background-size: 24px 24px;
}
```

## Palette item

```css
.palette-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  margin-bottom: 5px;
  border-radius: 9px;
  border: 1px solid transparent;
  background: var(--surface);
  cursor: grab;
  transition: all 0.2s;
  user-select: none;
}

.palette-item:hover {
  border-color: var(--border-glow);
  background: var(--surface-hover);
  box-shadow: 0 0 12px rgba(56, 189, 248, 0.12);
}

.palette-item .icon-wrap {
  width: 26px;
  height: 26px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--cyan);
}

.palette-hint {
  margin-top: 10px;
  padding: 10px;
  border-radius: 8px;
  background: rgba(2, 128, 144, 0.1);
  border: 1px solid rgba(2, 128, 144, 0.22);
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
  filter: drop-shadow(0 0 8px rgba(56, 189, 248, 0.8));
}

.wire-pulse {
  fill: none;
  stroke: var(--cyan);
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
  fill: var(--cyan);
  opacity: 0;
  filter: drop-shadow(0 0 6px var(--cyan));
}

.wire-particle.animating { opacity: 1; }
```

## Filled card (node or slot)

```css
.node, .slot.filled {
  background: linear-gradient(145deg, #131f3d 0%, var(--surface) 100%);
  border: 1.5px solid var(--border);
  border-radius: 12px;
}

.node .node-icon, .slot-icon {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(56, 189, 248, 0.1);
  border-radius: 7px;
  color: var(--cyan);
}
```

## Empty slot + validation states

```css
.slot.empty {
  border: 2px dashed rgba(56, 189, 248, 0.35);
  background: rgba(17, 27, 54, 0.55);
  animation: slot-pulse 2.5s ease infinite;
}

.slot.drop-target {
  border-color: var(--cyan) !important;
  box-shadow: 0 0 22px rgba(56, 189, 248, 0.35);
  transform: scale(1.04);
}

.slot.error {
  border-color: var(--error) !important;
  box-shadow: 0 0 20px rgba(239, 83, 80, 0.45);
  animation: shake 0.45s ease;
}

.slot.warning {
  border-color: var(--warning) !important;
  box-shadow: 0 0 18px rgba(255, 184, 77, 0.35);
}

.slot.success-flash {
  border-color: var(--success) !important;
  box-shadow: 0 0 22px rgba(2, 195, 154, 0.45);
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(-6px); }
  40% { transform: translateX(6px); }
  60% { transform: translateX(-4px); }
  80% { transform: translateX(4px); }
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
  background: rgba(17, 27, 54, 0.94);
  border: 1px solid var(--border);
  font-size: 0.76rem;
  color: var(--text-muted);
  z-index: 10;
  text-align: center;
}

#status.active { color: var(--cyan); }
#status.error { color: var(--error); border-color: rgba(239, 83, 80, 0.4); }
#status.success { color: var(--success); border-color: rgba(2, 195, 154, 0.4); }

#icon-sprites { display: none; }
```
