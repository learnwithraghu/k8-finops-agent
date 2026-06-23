# K8s FinOps Agent - Skill for Creating Presentation SVGs

## Purpose

This skill provides PPT-safe SVG rules and a legacy checklist for presentation decks (PowerPoint, Keynote, Google Slides).

**For full slide workflows (plan → pencil-sketch SVG → QA), use `finops-slide-visuals/SKILL.md` first.** It is modeled on the [substack-visuals](https://github.com/learnwithraghu/substack/tree/main/skills/substack-visuals) skill pattern with repo-specific Teal Trust styling and Section 05 gold-standard references.

### Integration with FinOps Slide Visuals

Primary workflow skill: `.kilo/skills/finops-slide-visuals/SKILL.md`

Reference files (read as needed):
- `references/style-dna.md` — white pencil-sketch aesthetic
- `references/visual-types.md` — slide type picker
- `references/composition-patterns.md` — FinOps layout patterns
- `references/svg-recipes.md` — copy-paste SVG snippets
- `references/qa-checklist.md` — post-edit gate

### Integration with Infographic & Metaphor Skill

The `infographic-metaphor` skill (located at `.kilo/skills/infographic-metaphor.md`) provides fast metaphor parameters for a single slide. When ideating, invoke it like:

```markdown
{{% call_skill "infographic-metaphor"
   title="Connecting K8s Metadata to FinOps"
   metaphor="bridge"
   components=["cluster","json","python-agent"]
   palette="aws"
%}}
```

This will generate a description and a ready‑to‑use SVG (e.g., `slides/bridge_k8s_finops.svg`) that you can embed directly into your presentation.
## When to Use

Use this skill when:
- Creating new visual slides for sections
- Designing architecture flow diagrams
- Visualizing data payloads or JSON outputs
- Explaining complex code logic comparisons
- Adding interactive or diagnostic slide blocks

## Workflow & Guidelines

### Step 1: Canvas & Aspect Ratio Setup
Always use a standard **16:9 widescreen** canvas for slides. Set the outer container with a responsive width/height and a clear `viewBox` matching standard dimensions:
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="100%" height="100%">
  <!-- Background -->
  <rect width="1280" height="720" fill="#FFFFFF" />
  ...
</svg>
```

### Step 2: Establish the Tech Color Palette

**Teal Trust** (default for Section 05+):
| Token | Hex | Use |
|-------|-----|-----|
| Slide bg | `#FFFFFF` | Full canvas |
| Charcoal text | `#232F3E` | Titles, pencil strokes |
| Muted | `#607D8B` | One subtitle line |
| Primary teal | `#028090` | Accents, active cards, arrows |
| Seafoam | `#00A896` | Secondary highlights |
| Mint | `#02C39A` | Success / winner highlight |
| Warm | `#FFB84D` | Policy / YAML emphasis |
| Card fill | `#FAFAFA` | Light sketch panels |
| Warning | `#EF5350` | Violations / crosses |

**Pencil sketch (Section 05+ default):** hand-drawn `<path>` panels, white background, minimal lines, max 40 words. See `finops-slide-visuals/references/style-dna.md`.

**Legacy dark variant (deprecated for new Section 05+ work):** do not use `#0B1020` stage layouts for new slides. Rework existing dark slides to white pencil sketch when touching a deck.

**AWS/GCP** (legacy sections):
- **Base Text / Charcoal**: `#232F3E` (AWS Charcoal) or `#37474F` (GCP Slate)
- **Primary / Action Blue**: `#4285F4` (GCP Blue) or `#1E88E5`
- **Exclusion / Config Orange**: `#FF9900` (AWS Orange) or `#B78103`
- **Success / Compliance Green**: `#34A853` (GCP Green) or `#2E7D32`
- **Warning / Non-compliance Red**: `#EF5350` or `#C62828`
- **Card Backgrounds**: Light neutral tints like `#F8F9FA` or `#ECEFF1`

### Step 3: Embed Lucide Icons Inline

Use [Lucide icons](https://lucide.dev/icons/) for UI metaphors. Copy the SVG path from lucide.dev, normalize to a 24×24 viewBox, and place in `<defs>`:

```xml
<defs>
  <g id="lucide-brain">
  <path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z" fill="none" stroke="#028090" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z" fill="none" stroke="#028090" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
</defs>
<!-- Place at (x,y) with 24px size: -->
<use href="#lucide-brain" x="100" y="200" width="24" height="24"/>
```

Keep custom K8s icons (hexagon pod, YAML doc) alongside Lucide for domain-specific metaphors.

### Step 4: Leverage Reusable Icon Definitions
Do not draw shapes ad-hoc inside the code body. Instead, declare standard icons inside a `<defs>` block at the top of the file, then reference them with `<use href="#icon-id" x="..." y="..." />`.

Common project icons:
```xml
<defs>
  <!-- Hexagon Pod/Workload Icon -->
  <g id="icon-pod">
    <polygon points="0,-16 13.86,-8 13.86,8 0,16 -13.86,8 -13.86,-8" fill="none" stroke="#E57373" stroke-width="1.8" />
    <line x1="0" y1="-16" x2="0" y2="16" stroke="#E57373" stroke-width="1" opacity="0.4" />
    <line x1="0" y1="0" x2="13.86" y2="8" stroke="#E57373" stroke-width="1" opacity="0.4" />
    <line x1="0" y1="0" x2="-13.86" y2="8" stroke="#E57373" stroke-width="1" opacity="0.4" />
  </g>
  
  <!-- ConfigMap / YAML Document Icon -->
  <g id="icon-cm">
    <path d="M -9,-12 L 3,-12 L 9,-6 L 9,12 L -9,12 Z" fill="none" stroke="#FFB300" stroke-width="1.5" />
    <path d="M 3,-12 L 3,-6 L 9,-6" fill="none" stroke="#FFB300" stroke-width="1.5" />
    <line x1="-5" y1="-2" x2="5" y2="-2" stroke="#FFB300" stroke-width="1.2" opacity="0.8" />
  </g>

  <!-- Warning / Danger Icon -->
  <g id="icon-warning">
    <polygon points="0,-12 12,8 -12,8" fill="#EF5350" stroke="#EF5350" stroke-width="1.5" />
    <circle cx="0" cy="5" r="1.2" fill="#ffffff" />
    <line x1="0" y1="-5" x2="0" y2="2" stroke="#ffffff" stroke-width="2" stroke-linecap="round" />
  </g>
</defs>
```

### Step 5: PPT-Safe SVG Rules (Convert to Shape)

PowerPoint's "Convert to Shape" breaks on overlapping or complex SVG. Enforce:

1. **Safe zone**: All content inside `x=80..1200, y=100..660`
2. **No overlaps**: Minimum 24px gap between sibling elements
3. **Animation groups**: Wrap each animatable unit in `<g id="anim-{name}">`
4. **Text isolation**: Each label in its own `<g>`; 8px inset from card edges
5. **No filters/masks/clippath**
6. **Gradients**: Max 1 per slide; prefer flat fills for cards
7. **Lines**: Separate `<line>`/`<path>` elements, not shared borders with text
8. **Text budget**: Max 40 visible words per slide

### Step 5B: Make It Feel Premium (Pencil Sketch)

If a slide looks "fine" but not memorable, push it further:
- Use a **dominant visual metaphor** first, supporting labels second
- Prefer **big-icon or hub anchors** over many small cards
- Give each slide **one focal region** (~35–45% of canvas)
- Use **hand-drawn paths and whitespace**, not dark layers or shadow stacks
- Vary layout types across the section (split, hub, rail, before/after) — not the same card grid
- For before/after slides, tint and badge the two states (red BEFORE vs mint AFTER)

### Step 6: Keep Connections & Lines Clean ("No Spaghetti")
- **Avoid Crossing Lines**: Prevent lines from intersecting. Instead of drawing a complex maze of connections, align components vertically or horizontally and use straight or clear curved lines.
- **Dashed vs. Solid**: Use solid lines for primary active routing (e.g. data pipelines) and dashed lines for logic references or validations.
- **Arrows**: Add small polygons as arrowheads at the ends of connection paths for clear flow direction.

### Step 7: Code Annotations & Diagnostic Callouts
When showing file contents or JSON snippets (e.g., metadata structures):
- Display the snippet in a stylized IDE window container (complete with browser control dots).
- Draw highlighting rects over key properties.
- Connect highlighted properties directly to colored inspector/diagnostic cards using dotted lines to immediately explain the business logic associated with the property.

---

## Checklist

- [ ] Does the SVG use the `viewBox="0 0 1280 720"` standard?
- [ ] White canvas + Teal Trust accents (Section 05+); title at `x=80,y=88` without dark title bar?
- [ ] Pencil-sketch hand-drawn panels (irregular paths, not dark stacked cards)?
- [ ] Does the slide have a clear focal point within 2 seconds of viewing?
- [ ] Are Lucide icons inlined in `<defs>` and placed via `<use>`?
- [ ] Is typography consistent (`Arial` or system-ui sans-serif)?
- [ ] Are all fonts set with absolute sizes to avoid scaling rendering issues?
- [ ] Are vector icons defined in `<defs>` and reused with `<use>`?
- [ ] Are animatable elements wrapped in `<g id="anim-*">` groups?
- [ ] Is visible text ≤ 40 words per slide?
- [ ] Are connections straight, parallel, or neatly curved (no intersecting lines)?
- [ ] Is content inside safe zone (`x=80..1200, y=100..660`) with 24px gaps?
- [ ] No filters, masks, or clippath?
- [ ] Does the SVG scale responsively inside PPT via `width="100%"` and `height="100%"`?
- [ ] **Redo-in-place**: edit existing slide files; do not add new files unless approved
- [ ] Does this feel like a presentation slide, not an app mockup with a title pasted on top?
