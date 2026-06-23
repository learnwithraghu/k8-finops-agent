# Infographic & Metaphor Thinking Skill

**Skill ID:** `infographic-metaphor`

**Purpose:**
Provide a fast metaphor-first ideation pass for a single slide. For the full workflow (visual plan, pencil-sketch SVG, QA, `presentation_guide.md`), use **`finops-slide-visuals/SKILL.md`**.

**Key Steps**
1. **Clarify the Core Message** – Define the single sentence that captures the concept.
2. **Select a Metaphor** – Choose a relatable analogy (e.g., "bridge", "pipeline", "maze").
3. **Map Elements to Visual Tokens** – Identify reusable SVG icons (cluster, JSON, brain, Python agent, etc.) and palette colors.
4. **Design Layout** – Decide on a 16:9 canvas, split‑screen or layered flow, and placement of titles, icons, arrows.
5. **Generate SVG Snippets** – Use Lucide inline paths (see mapping below) and embed in `<defs>`.
6. **Assemble & Export** – Combine snippets into a final SVG; wrap each step in `<g id="anim-*">` for PPT animation.

**Parameters**
- `title` – Short slide title (max 6‑8 words).
- `metaphor` – Chosen metaphor term (e.g., "bridge", "pipeline", "maze").
- `components` – List of visual components to include (e.g., `cluster`, `json`, `python-agent`).
- `palette` – Optional custom color palette; defaults to **Teal Trust** for Section 05+.

**Teal Trust Palette** (Section 05+ default)
| Token | Hex |
|-------|-----|
| Title bar | `#21295C` |
| Primary teal | `#028090` |
| Seafoam | `#00A896` |
| Mint | `#02C39A` |
| Charcoal | `#232F3E` |
| Muted | `#607D8B` |
| Card fill | `#F2F2F2` |
| Warning | `#EF5350` |

**Lucide Icon Mapping** (from [lucide.dev](https://lucide.dev/icons/))

| Metaphor component | Lucide icon |
|--------------------|-------------|
| cluster / K8s | `hexagon` or custom pod icon |
| json / data | `file-json` or `braces` |
| python-agent | `bot` |
| brain / LLM | `brain` |
| policy / rules | `file-text`, `settings-2` |
| cloud provider | `cloud` |
| adapter / chain | `link`, `workflow` |
| folder / workspace | `folder-tree` |
| model config | `sliders-horizontal`, `key` |
| endpoint | `globe` |
| success | `check`, `circle-check` |
| failure | `x`, `triangle-alert` |
| flow direction | `arrow-right` |
| open question | `circle-question-mark` |
| ticket / report | `clipboard-list` |
| enhancement | `sparkles` |

**Animation Groups**
- Pipeline metaphors: `anim-step-1` … `anim-step-N` for sequential PPT reveals
- Comparison metaphors: `anim-card-left`, `anim-card-right`, `anim-vs-badge`
- Fusion metaphors: `anim-input-a`, `anim-input-b`, `anim-reactor`, `anim-output`

**Premium Composition Rules**
- Pick one of these framing patterns before drawing: `hero-plus-support`, `split-screen`, `center-stage`, or `timeline`
- Give the metaphor a **large stage presence**: it should occupy at least 35-45% of the slide
- Supporting labels should sit in small side rails or cards, not compete with the metaphor
- If the slide explains a transition, make the left and right halves feel visually different in tone
- Prefer bold silhouettes, rings, rails, and stage panels over many equal-sized floating cards

**Example Usage** (in another skill):
```markdown
{{% call_skill "infographic-metaphor" 
   title="Connecting K8s Metadata to FinOps" 
   metaphor="bridge" 
   components=["cluster","json","python-agent"] 
   palette="teal-trust" 
%}}
```
The skill will output a Markdown block with a description of the visual layout and a reference to the generated SVG file (e.g., `slides/slide6_fusion.svg`).

**Outputs**
- `description.md` – Short narrative explaining the infographic.
- `slide.svg` – Final SVG ready for inclusion in the presentation.

**Integration Tips**
- Store generated SVGs under `sections/{NN}-{section}/slides/`.
- The repository already has a `skills` symlink pointing to `.kilo/skills/`.
- Update `create-presentation-svgs.md` to call this skill whenever a metaphor‑driven slide is needed.
- **Redo-in-place**: edit existing slide files; do not add new slide files unless user approves.

---
*This skill file is concise for quick reference. Extend or adapt as your visual design needs evolve.*
