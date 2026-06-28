---
name: architecture-builder-visuals
description: >-
  Builds single-file HTML drag-and-drop architecture builder UIs for k8-finops-agent
  teaching — AWS light canvas (white + amber), shuffled palette, story hints on slots,
  pan/zoom, Run Flow validation. Use when creating or extending architecture_builder/index.html,
  interactive pipeline builders, placeholder slot games, or when the user asks for
  the architecture builder look and feel.
---

# Architecture Builder Visuals

## Purpose

Create **single-file HTML** (`index.html`, zero dependencies) interactive architecture builders for students.

**Canonical reference (copy this first):**

[`sections/01-cluster-foundation/architecture_builder/index.html`](../../../sections/01-cluster-foundation/architecture_builder/index.html) — placeholder slots, story hints, shuffled palette, pan/zoom, AWS light theme, Run Flow validation.

**Legacy exception (do not copy for new section builders):**

[`visual-learning/visuals/rag_architecture_builder/index.html`](../../../visual-learning/visuals/rag_architecture_builder/index.html) — dark cyber canvas, pre-wired nodes, free reconnect. Keep as-is unless explicitly migrating.

**Not** the white pencil-sketch slide style — that is [`finops-slide-visuals`](../finops-slide-visuals/SKILL.md).

## When to use

- User asks for an architecture builder, pipeline game, drag-and-drop flow UI
- Adding a new section `architecture_builder/index.html`
- Extending Run Flow, wire glow, palette, slot validation, or canvas navigation
- User says "same style as the cluster foundation builder" or "architecture builder palette"

## Reference files

- [style-dna.md](references/style-dna.md) — AWS light palette (default), legacy dark, typography, mood
- [css-base.md](references/css-base.md) — copy-paste `:root` tokens and core CSS (**AWS light**)
- [interaction-patterns.md](references/interaction-patterns.md) — modes, story hints, palette shuffle, pan/zoom, Run Flow

Read references before building. **Do not invent a new palette** for section builders.

## Theme rule

| Builder location | Theme | Reference |
|------------------|-------|-----------|
| `sections/*/architecture_builder/` | **AWS light** (white canvas, amber accent) | Section 01 builder |
| `visual-learning/visuals/*_architecture_builder/` | Legacy dark cyber (unless user asks to migrate) | RAG builder |

New section builders must use AWS light tokens from [css-base.md](references/css-base.md). Aligns with [finops-slide-visuals palette-by-section](../finops-slide-visuals/references/palette-by-section.md) Sections 01–04.

## Delivery checklist

1. **One HTML file** — inline CSS + JS + SVG icon sprites; no CDN, no build step
2. **Copy `:root` tokens** from [css-base.md](references/css-base.md) verbatim (AWS light)
3. **Layout shell**: toolbar → palette (left) → `#canvas-wrap` → `#canvas-viewport` → `#canvas` (dot grid + `#zones-layer` + `#wire-layer` + slots) → zoom controls → status bar
4. **Icons**: Lucide-inspired `<symbol>` defs in hidden `#icon-sprites`; use via `<svg><use href="#icon-id"/></svg>`
5. **Palette**: dual list — **Available** (unplaced, shuffled) + **On canvas** (placed, draggable to reassign); reshuffle Available order on Reset
6. **Hint callout**: toolbar **Need a hint?** + `HINT_TIERS` per slot; floating `#hint-callout` anchored near the target slot (not in palette); auto-fades after 10s
7. **Auto Solve**: toolbar button fills only wrong/empty slots with fly animation, then runs validation
8. **Empty slots (Mode B)**: Step number + `storyHint` (plain-language domain line — not component name)
9. **Pan/zoom**: drag canvas background to pan; wheel + −/+ Fit Center controls; auto-fit on load and Reset; disable while Run Flow runs
10. **Run action**: grouped or sequential validation with wire pulse; button label matches section (`Run Flow`, `Run Audit`, `Collect Snapshot`, etc.)
11. **Layout archetype**: pick one per section from [interaction-patterns.md](references/interaction-patterns.md) — do not copy Section 01's timeline chain for every section
12. **Reset** clears slots, re-shuffles Available order, clears hint tiers, hides hint callout, re-centers view
13. Link from the section guide (`N_guide.md`) with open instructions

## Two builder modes

| Mode | Use when | Reference |
|------|----------|-----------|
| **Template + edit** | Pre-wired diagram students rearrange/reconnect | RAG builder (dark legacy) |
| **Placeholder slots** | Empty slots; student fills; Run validates correctness | Section 01 builder (AWS light) |

Pick one per builder. Do not mix free canvas placement with slot validation in the same file without clear UX separation.

## File placement

- Section-specific: `sections/{NN}-{section}/architecture_builder/index.html`
- Cross-cutting demo: `visual-learning/visuals/{name}_architecture_builder/index.html`

## Related skills

- `finops-slide-visuals` — static SVG slides; shares AWS/charcoal tokens for Sections 01–04
- Do not apply slide pencil-sketch rules to architecture builders
