---
name: architecture-builder-visuals
description: >-
  Builds single-file HTML drag-and-drop architecture builder UIs for k8-finops-agent
  teaching — dark cyber canvas, glowing wire animations, palette + slots/nodes,
  Run Flow validation. Use when creating or extending architecture_builder/index.html,
  interactive pipeline builders, placeholder slot games, or when the user asks for
  the architecture builder look and feel.
---

# Architecture Builder Visuals

## Purpose

Create **single-file HTML** (`index.html`, zero dependencies) interactive architecture builders for students. Same visual language as:

- [`visual-learning/visuals/rag_architecture_builder/index.html`](../../../visual-learning/visuals/rag_architecture_builder/index.html) — pre-wired draggable nodes
- [`sections/01-cluster-foundation/architecture_builder/index.html`](../../../sections/01-cluster-foundation/architecture_builder/index.html) — empty placeholder slots + validation

**Not** the white pencil-sketch slide style — that is [`finops-slide-visuals`](../finops-slide-visuals/SKILL.md). Architecture builders use a **dark game-like canvas**.

## When to use

- User asks for an architecture builder, pipeline game, drag-and-drop flow UI
- Adding a new section `architecture_builder/index.html`
- Extending Run Flow, wire glow, palette, or slot validation patterns
- User says "use the same style as the RAG builder" or "architecture builder palette"

## Reference files

- [style-dna.md](references/style-dna.md) — palette, typography, mood, bans
- [css-base.md](references/css-base.md) — copy-paste `:root` tokens and core CSS
- [interaction-patterns.md](references/interaction-patterns.md) — two builder modes, wires, Run Flow, file structure

Read references before building. Do not invent a new palette.

## Delivery checklist

1. **One HTML file** — inline CSS + JS + SVG icon sprites; no CDN, no build step
2. **Copy `:root` tokens** from [css-base.md](references/css-base.md) verbatim
3. **Layout shell**: toolbar → palette (left) → canvas (dot grid + wire SVG layer + nodes/slots layer) → status bar
4. **Icons**: Lucide-inspired `<symbol>` defs in hidden `#icon-sprites`; use via `<svg><use href="#icon-id"/></svg>`
5. **Run Flow**: sequential wire pulse + particle via `requestAnimationFrame`; `.btn-primary.running` while active
6. **Reset** restores initial state
7. Link from the section guide (`N_guide.md`) with open instructions

## Two builder modes

| Mode | Use when | Reference |
|------|----------|-----------|
| **Template + edit** | Pre-wired diagram students rearrange/reconnect | RAG builder |
| **Placeholder slots** | Empty slots; student fills; Run validates correctness | Section 01 builder |

Pick one per builder. Do not mix free canvas placement with slot validation in the same file without clear UX separation.

## File placement

- Section-specific: `sections/{NN}-{section}/architecture_builder/index.html`
- Cross-cutting demo: `visual-learning/visuals/{name}_architecture_builder/index.html`

## Related skills

- `finops-slide-visuals` — static SVG slides (white background); different aesthetic
- Do not apply slide pencil-sketch rules to architecture builders
