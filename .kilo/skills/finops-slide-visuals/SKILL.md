---
name: finops-slide-visuals
description: >-
  Creates white-background pencil-sketch SVG presentation slides for K8s FinOps
  Agent sections — metaphors, pipelines, before/after, and workspace maps.
  Use when creating or reworking section slides, deck visuals, architecture
  diagrams, or when the user asks for presentation SVGs, slide graphics, or
  FinOps teaching visuals.
---

# FinOps Slide Visuals

## Purpose

Create and refine **16:9 SVG slides** for section presentation decks in this repo: white canvas, hand-drawn pencil outlines, Teal Trust accents, Lucide icons, and `anim-*` groups for PowerPoint step reveals.

Default delivery: **visual plan → SVG in place → QA → update `presentation_guide.md`**.

Read section `guide.md` and existing slides in `sections/{NN}-{section}/slides/` before drawing. For palette and SVG mechanics, read reference files only as needed — do not load them all at once.

## Reference files

- [style-dna.md](references/style-dna.md) — pencil-sketch aesthetic, color, typography, bans
- [visual-types.md](references/visual-types.md) — when to use metaphor vs pipeline vs before/after
- [composition-patterns.md](references/composition-patterns.md) — FinOps/K8s layout patterns
- [svg-recipes.md](references/svg-recipes.md) — hand-drawn paths, Lucide defs, anim groups
- [palette-by-section.md](references/palette-by-section.md) — Teal Trust vs legacy AWS/GCP
- [qa-checklist.md](references/qa-checklist.md) — post-edit quality gate

## Related skills

- `create-presentation-svgs.md` — PPT-safe SVG rules and legacy checklist
- `infographic-metaphor.md` — quick metaphor parameters for a single slide

Invoke **this skill first** for full slide workflows. Use `infographic-metaphor` for fast single-slide ideation, then implement here.

## Inputs

Expected inputs:
- section number and topic (e.g. `05-llm-agent-langchain`)
- narration goal from `sections/{NN}-{section}/guide.md` or `slides/presentation_guide.md`
- existing slide file to redo in place (preferred) or approved new filename
- optional: which `anim-*` groups need step-by-step PPT reveals

## When to use

Use this skill when:
- creating or reworking slides under `sections/*/slides/*.svg`
- user asks for pencil sketch, white background, or cleaner deck visuals
- converting dark/corporate slides to the repo's current style
- adding before/after, pipeline, or harness-comparison slides

Skip only if the user explicitly wants raster/AI-generated images instead of SVG.

## Core rules

- **Output format**: editable SVG (`viewBox="0 0 1280 720"`, `width="100%"`, `height="100%"`).
- **Canvas**: pure white `#FFFFFF` for Section 05+; legacy sections may use white cards on white (see palette reference).
- **One idea per slide**. Max **40 visible words** on the slide face.
- **Pencil sketch**: wobbly `<path>` borders, round caps/joins, light fills — not perfect `<rect>` UI chrome.
- **Minimal lines**: no tree connectors, spaghetti arrows, or duplicate shadow layers.
- **Redo in place**: edit existing `slide*.svg` files; do not add new slide files unless the user approves.
- **PPT-safe**: no filters, masks, or clippath; icons in `<defs>` + `<use>`; content in safe zone `x=80..1200, y=100..660`.
- **No fabricated metrics** on comparison slides unless present in section code or guide.

## Workflow

Copy this checklist and track progress:

```
Task Progress:
- [ ] Step 1: Read section narrative and find the one slide idea
- [ ] Step 2: Write slide visual plan (shot list)
- [ ] Step 3: Choose visual type and composition pattern
- [ ] Step 4: Sketch layout (metaphor + labels)
- [ ] Step 5: Build or rework SVG in place
- [ ] Step 6: QA with checklist
- [ ] Step 7: Update presentation_guide.md if needed
```

### Step 1 — Digest and anchor

Read once for:
- the single sentence the slide must land
- whether this is **concept**, **flow**, **comparison**, **workspace map**, or **before/after**
- which `anim-*` groups the presenter will reveal step-by-step

Prioritize **cognitive anchors**: parser vs LLM, harness shootout, prompt fusion, pipeline blocks, raw scan vs decision report.

### Step 2 — Slide visual plan

Before editing SVG, write a short plan. For a single slide, inline in chat; for a section batch, save to:

`sections/{NN}-{section}/slides/.plans/{slide-name}-visual-plan.md`

```markdown
# Slide Visual Plan

## Slide
- File: sections/05-llm-agent-langchain/slides/slide6_fusion.svg
- Title: Prompt Beats Parsers
- Source: presentation_guide.md slide 2

## Type
- flow diagram | metaphor | before/after | comparison | workspace map

## Core idea
One sentence the viewer should remember.

## Composition pattern
e.g. three inputs → fusion hub → output card

## Labels (max 6)
- system prompt
- tagging-rules.yaml
- resource facts
- PROMPT_TEMPLATE
- LLM decision

## Animation groups
- anim-input-system, anim-input-yaml, anim-input-facts, anim-reactor, anim-output

## Palette
- teal-trust (Section 05+)
```

### Step 3 — Choose visual type

See [visual-types.md](references/visual-types.md).

| Signal in section narrative | Visual type |
|-----------------------------|-------------|
| Abstract gap (data without decisions) | Split metaphor cards |
| Multi-input fusion | Flow into hub |
| Framework/vendor choice | Comparison cards + winner |
| Code workspace | Flat file list + 2–3 callouts |
| Pipeline / chain | Horizontal step rail |
| Section transition | Before/after terminal or report |

When in doubt, prefer **one focal metaphor** over many equal cards.

### Step 4 — Invent the layout

Follow [composition-patterns.md](references/composition-patterns.md):

1. Name the FinOps concept (orphan PVC, alias mismatch, prompt fusion, harness lock-in).
2. Map to a physical or operational image (leaky parser, three inputs into one brain, vendor clouds vs one adapter).
3. Pick **≤5 labeled regions** and one hero element occupying 35–45% of the slide.
4. Compose with whitespace; let icons carry detail text would otherwise duplicate.

### Step 5 — Build SVG

Implement with recipes from [svg-recipes.md](references/svg-recipes.md).

**File location:**

```text
sections/{NN}-{section}/slides/
  slide{N}_{topic}.svg
  presentation_guide.md
  .qa/{slide}.png          # optional rsvg-convert preview
```

**SVG skeleton:**

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="100%" height="100%">
  <defs><!-- Lucide + domain icons --></defs>
  <rect width="1280" height="720" fill="#FFFFFF"/>
  <g id="anim-titlebar"><!-- title + one subtitle line --></g>
  <g id="anim-{focal}"><!-- hero metaphor --></g>
</svg>
```

Use hand-drawn panel paths instead of stacked dark cards:

```xml
<path d="M 4 8 L 518 5 L 522 348 L 6 352 Z"
      fill="#FAFAFA" stroke="#232F3E" stroke-width="2.2"
      stroke-linecap="round" stroke-linejoin="round"/>
```

**Optional QA preview:**

```bash
rsvg-convert -w 1280 -h 720 sections/05-llm-agent-langchain/slides/slide1_goal.svg \
  -o sections/05-llm-agent-langchain/slides/.qa/slide1_goal.png
```

### Step 6 — QA and iterate

Run [qa-checklist.md](references/qa-checklist.md).

Regenerate or simplify if:
- slide feels like a dark SaaS dashboard or corporate infographic
- too many lines, labels, or nested cards
- crossing arrows or tree connector spaghetti
- text exceeds 40 words or duplicates narration script
- PowerPoint would break on filters/overlapping complexity

Prefer **removing** elements over adding decoration.

### Step 7 — Wire into section package

Update `slides/presentation_guide.md` when:
- slide title or narrative order changes
- new `anim-*` groups are added
- design system notes change

Keep presentation order table aligned with filenames.

## Gold-standard references in this repo

Study these before reworking a section deck:

| Pattern | Reference slide |
|---------|-----------------|
| Split problem/solution | `sections/05-llm-agent-langchain/slides/slide1_goal.svg` |
| Multi-input fusion | `sections/05-llm-agent-langchain/slides/slide6_fusion.svg` |
| Harness shootout | `sections/05-llm-agent-langchain/slides/slide2_frameworks.svg` |
| Hub + pillars | `sections/05-llm-agent-langchain/slides/slide3_langchain_features.svg` |
| Flat workspace map | `sections/05-llm-agent-langchain/slides/slide4_file_structure.svg` |
| Pipeline rail | `sections/05-llm-agent-langchain/slides/slide7_pydantic.svg` |
| Before/after | `slide8a_raw_scan.svg` → `slide8b_llm_report.svg` |

## Output summary

Deliver briefly:
- which slide file(s) were edited
- visual type and composition pattern used
- word count estimate and anim groups preserved
- any QA simplifications made

Do not write long design theory. Let the SVG and plan speak.

## Quality bar

A successful slide is:
- readable in 2 seconds at projector distance
- on-brand for K8s FinOps Agent (white pencil sketch + Teal Trust)
- honest to the section code and narration
- PPT animation-friendly via `anim-*` groups
- lighter than the narration — the presenter talks; the slide anchors

Target reaction: **the sketch lands the concept faster than another bullet list would**.
