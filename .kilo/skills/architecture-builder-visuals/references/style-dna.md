# Style DNA — Architecture Builder UIs

## One line (default — section builders)

A light interactive pipeline on a white dot-grid canvas — warm amber accents, charcoal text, story hints on empty slots.

Think: AWS console workbook for wiring up a cluster foundation, not a dark neon game or a pencil-sketch slide.

## Theme selection

| Theme | When | Reference |
|-------|------|-----------|
| **AWS light** (default) | All new `sections/*/architecture_builder/` | Section 01 builder |
| **Dark cyber** (legacy) | Existing RAG visual-learning builder only | `rag_architecture_builder/index.html` |

---

## AWS light — default for section builders

### Mood

- **Clean and teaching-first** — white canvas, readable contrast, warm amber highlights
- **Recall challenge** — shuffled palette, story hints describe *what* not *which tool*
- **Restrained accent** — amber on Run button, active wires, hover; no full-screen glow
- **Teaching clarity** — status bar guides; `VALIDATION_MESSAGES` teach on wrong picks

### Color tokens (required)

| Token | Hex | Use |
|-------|-----|-----|
| `--bg` | `#F4F6F8` | Page chrome |
| `--canvas-bg` | `#FFFFFF` | Canvas base |
| Canvas-wrap surround | `#EEF1F3` | Area around viewport |
| `--surface` | `#F8F9FA` | Cards, buttons, palette items |
| `--surface-hover` | `#FFF8F0` | Warm hover |
| `--border` | `#D5DBDB` | Default borders |
| `--accent` / `--border-glow` / `--wire-active` | `#FF9900` | AWS orange — CTA, wires, icons, hover |
| `--accent-dark` | `#EC7211` | Run button gradient end |
| `--text` | `#232F3E` | Charcoal body (AWS) |
| `--text-muted` | `#607D8B` | Subtitles, story hints |
| `--wire` | `#AAB7B8` | Default wire stroke |
| `--error` | `#EF5350` | Wrong component |
| `--warning` | `#FF9900` | Empty slot on Run |
| `--success` | `#34A853` | Step passed (GCP green, legacy pairing) |
| Empty slot fill | `#FFFBF2` | Warm policy tint |
| Diagram frame fill | `#FAFAFA` | `#canvas-frame` background |
| Dot grid | `#E8ECED` at 1px, 24px spacing | Canvas pattern |
| Palette sidebar | `#FFFFFF` | Left panel |
| Toolbar | `#FFFFFF` | Top bar |
| Palette item accent | `border-left: 3px solid rgba(255,153,0,0.65)` | Amber stripe |
| Icon wrapper tint | `rgba(255,153,0,0.1)` background, `color: var(--accent)` | Palette + slot icons |
| Palette hint box | `#FFFBF2` fill, `rgba(255,153,0,0.25)` border | Bottom of palette |

Shadow rgba (light bg — keep subtle):
- Amber hover: `rgba(255, 153, 0, 0.12–0.35)`
- Error: `rgba(239, 83, 80, 0.35)`
- Success: `rgba(52, 168, 83, 0.35)`

### Typography

- **Font stack**: `'Segoe UI', system-ui, -apple-system, sans-serif`
- **Title (toolbar h1)**: ~1.05rem, weight 700, **charcoal** `--text` (no gradient)
- **Subtitle**: 0.72rem, `--text-muted`
- **Palette header**: 0.68rem, uppercase, muted
- **Slot story hint**: 0.64rem, italic, `--text-muted`
- **Slot step label**: 0.58rem, uppercase, `--accent`
- **Node/slot labels (filled)**: 0.72rem, weight 600
- **Status**: 0.76rem; `.active` → amber, `.error` → red, `.success` → green

### Layout dimensions

| Token | Value | Use |
|-------|-------|-----|
| `--toolbar-h` | `56px` | Top bar |
| `--palette-w` | `210px` | Left sidebar |
| `--slot-w` | `150px` | Slot width |
| `--slot-h` | `84px` | Slot height (room for step + story hint) |
| `--node-w` / `--node-h` | `160px` / `72px` | Template mode nodes |
| Border radius | 8–16px cards, 8px buttons | Rounded panels |

### Visual components (AWS light)

**Toolbar** — white bg, charcoal title, amber `▶ Run Flow` gradient button.

**Canvas** — white dot grid; `#canvas-frame` rounded rect behind diagram rows (warm border + `#FAFAFA` fill); `#canvas-viewport` with pan/zoom transform on `#canvas`.

**Empty slots** — dashed amber border, `#FFFBF2` fill, pulse animation; show **Step N** + **storyHint** only.

**Filled slots** — white/`#F8F9FA` gradient card, charcoal border, soft amber shadow.

**Wires** — gray default; amber when active; particle uses `--accent`; lighter drop-shadow than dark theme.

**Status bar** — white pill, light border, subtle shadow; amber active state.

**Zoom controls** — floating bottom-right: −, +, Fit, Center.

---

## Dark cyber — legacy (RAG builder only)

Use only when extending `visual-learning/visuals/rag_architecture_builder/`. Do **not** use for new section builders.

| Token | Hex | Use |
|-------|-----|-----|
| `--bg` | `#0b1329` | Page + canvas |
| `--surface` | `#111b36` | Cards |
| `--cyan` | `#38bdf8` | Icons, active wires |
| `--teal` / `--teal-bright` | `#028090` / `#02c39a` | Buttons, success |

See RAG builder file for full dark CSS. Mood: game-like glowing bench, cyan wire travel.

---

## Icons

- **Source**: Lucide-inspired inline SVG `<symbol>` defs (MIT style)
- **Pattern**: hidden `#icon-sprites`; reference with `<use href="#icon-id"/>`
- **Stroke**: `currentColor`, width 2, round caps/joins
- **Color**: inherit `--accent` (AWS light) or `--cyan` (dark legacy)

## Absolutely avoid

- Inventing a third color system per builder
- Grouping palette into "correct" vs "distractor" sections (shuffle instead)
- Answer-revealing slot hints (`Container runtime`, `Docker`, etc.) — use `storyHint` domain lines
- External CDN fonts or icon libraries
- React/Vue/build steps for v1
- Mixing pencil-sketch slide rules with builder UI
- Applying dark cyber theme to new section builders unless user explicitly requests it

## Aesthetic direction

**Yes (section builders)**: white canvas, amber accents, story hints, shuffled palette, pan/zoom, teaching status messages

**No**: random pastels, corporate card grids, dark neon orbs, answer keys in slot labels
