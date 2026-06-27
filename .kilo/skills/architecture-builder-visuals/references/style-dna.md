# Style DNA — Architecture Builder UIs

## One line

A dark interactive pipeline game on a dot-grid canvas — glass cards, cyan wire glow, light traveling along connections.

Think: engineer wiring up a system on a glowing bench, not a whiteboard slide or SaaS marketing hero.

## Mood

- **Game-like but educational** — pulsing wires, particle travel, glow on hover
- **Dark cyber canvas** — deep navy background, teal/cyan accents
- **Restrained neon** — glow on active wires and hover states only, not full-screen effects
- **Teaching clarity** — status bar explains what to do; validation messages teach when wrong

## Color tokens

| Token | Hex | Use |
|-------|-----|-----|
| `--bg` | `#0b1329` | Page + canvas background |
| `--surface` | `#111b36` | Cards, buttons, palette items |
| `--surface-hover` | `#162040` | Hover states |
| Palette bg | `#0c152b` | Left sidebar |
| Toolbar gradient top | `#0e1830` | Toolbar fade into `--bg` |
| Node gradient start | `#131f3d` | Card gradient top-left |
| `--border` | `#2a3a60` | Default borders |
| `--border-glow` | `#38bdf8` | Hover border accent |
| `--teal` | `#028090` | Primary button gradient start, ports |
| Teal dark | `#036666` | Primary button gradient end |
| `--teal-bright` | `#02c39a` | Success, primary border, title gradient end |
| `--cyan` | `#38bdf8` | Icons, active wires, title gradient start |
| `--text` | `#e2e8f0` | Primary text |
| `--text-muted` | `#94a3b8` | Subtitles, hints, labels |
| `--wire` | `#1e4d6b` | Default wire stroke |
| `--wire-active` | `#38bdf8` | Active / animated wire |
| `--port` | `#028090` | Connection port fill |
| `--port-hover` | `#02c39a` | Port hover |
| `--error` | `#ef5350` | Wrong component, validation fail |
| `--warning` | `#ffb84d` | Empty slot on Run |
| `--success` | `#02c39a` | Step passed, completion message |
| Dot grid | `#1e293b` at 1px, 24px spacing | Canvas background pattern |

Glow rgba values used in box-shadows:
- Cyan hover: `rgba(56, 189, 248, 0.12–0.35)`
- Teal hint box: `rgba(2, 128, 144, 0.10–0.25)`
- Error: `rgba(239, 83, 80, 0.35–0.45)`
- Success: `rgba(2, 195, 154, 0.30–0.45)`

## Typography

- **Font stack**: `'Segoe UI', system-ui, -apple-system, sans-serif`
- **Title (toolbar h1)**: ~1.05–1.1rem, weight 700, letter-spacing -0.02em, **gradient text** cyan → teal-bright
- **Subtitle**: 0.72–0.75rem, `--text-muted`
- **Palette section headers**: 0.68–0.7rem, uppercase, letter-spacing 0.08em, muted
- **Node/slot labels**: 0.72–0.78rem, weight 600
- **Category/type sublabels**: 0.62rem, muted
- **Palette hints / status**: 0.68–0.76rem, muted; status turns cyan/error/success when active

## Layout dimensions

| Token | Value | Use |
|-------|-------|-----|
| `--toolbar-h` | `56px` | Top bar |
| `--palette-w` | `200–210px` | Left sidebar |
| `--node-w` / `--slot-w` | `150–160px` | Card width |
| `--node-h` / `--slot-h` | `72–76px` | Card height |
| Icon wrap (palette) | 26–28px box, 18–20px SVG | Palette items |
| Icon wrap (node/slot) | 30–32px box, 18–20px SVG | Canvas cards |
| Border radius | 8–14px cards, 8–10px buttons | Rounded glass panels |

## Visual components

### Toolbar
- Gradient `#0e1830 → --bg`, bottom border `--border`
- Left: gradient title + muted subtitle ("Drag · Connect · Run" or similar)
- Right: `Reset` (secondary `.btn`) + `▶ Run Flow` (`.btn-primary`)

### Canvas
- Dot-grid background on `--bg`
- `#wire-layer` SVG behind nodes/slots (z-index 1)
- `#nodes-layer` or `#slots-layer` on top (z-index 2)

### Cards (nodes / filled slots)
- `linear-gradient(145deg, #131f3d, --surface)`
- Border 1.5px `--border`, radius 12–14px
- Hover: cyan border tint + soft glow
- Icon in tinted cyan box: `rgba(56, 189, 248, 0.1)` background

### Empty slots (placeholder mode)
- Dashed border `rgba(56, 189, 248, 0.35)`, subtle pulse animation
- Step number + hint text centered
- `.drop-target`: cyan border + scale 1.04 + glow

### Wires
- Cubic bezier, default `--wire` 2px
- Active: `--wire-active` 3px + `drop-shadow` glow
- Pulse overlay: `--cyan` 4px, `stroke-dasharray: 12 200`, `@keyframes wire-travel`
- Particle: 5px circle, cyan fill + drop-shadow, animated along path via `getPointAtLength`

### Status bar
- Fixed/floating bottom center, pill shape
- Background `rgba(17, 27, 54, 0.92–0.94)`, border `--border`
- States: default (muted), `.active` (cyan), `.error` (red), `.success` (green)

## Icons

- **Source**: Lucide-inspired inline SVG `<symbol>` defs (MIT style)
- **Pattern**: hidden `#icon-sprites` at end of body; reference with `<use href="#icon-id"/>`
- **Stroke**: `currentColor`, width 2, round caps/joins
- **Color**: inherit `--cyan` on icon wrappers

## Absolutely avoid

- White slide backgrounds (that's finops-slide-visuals)
- External CDN fonts or icon libraries
- React/Vue/build steps for v1
- Heavy full-screen neon orbs, robot mascots, stock AI brain art
- More than one visual system per file (don't mix slide sketch + dark canvas)

## Aesthetic direction

**Yes**: dark dot grid, glass cards, traveling light on wires, palette sidebar, teaching status messages

**No**: corporate light infographic, PPT-exported slides, generic n8n clone with rounded pastels
