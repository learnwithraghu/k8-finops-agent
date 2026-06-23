# SVG Recipes — Pencil Sketch Slides

Copy-adapt these snippets. Always keep PPT-safe rules: no filters, masks, or clippath.

## Canvas shell

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" width="100%" height="100%">
  <defs>
    <!-- Lucide icons here -->
  </defs>
  <rect width="1280" height="720" fill="#FFFFFF"/>
  <g id="anim-titlebar">
    <text x="80" y="88" font-family="Arial, sans-serif" font-size="40" font-weight="bold" fill="#232F3E">Slide Title</text>
    <text x="80" y="128" font-family="Arial, sans-serif" font-size="20" fill="#607D8B">One subtitle line only.</text>
  </g>
  <!-- focal groups -->
</svg>
```

## Hand-drawn panel (sketch rect)

Slightly irregular corners — adjust coordinates per panel size:

```xml
<path d="M 4 8 L 518 5 L 522 348 L 6 352 Z"
      fill="#FAFAFA" stroke="#232F3E" stroke-width="2.2"
      stroke-linecap="round" stroke-linejoin="round"/>
```

Tinted variants:
- Policy: `fill="#FFFBF2" stroke="#FFB84D"`
- Failure: `fill="#FFF8F8" stroke="#EF5350"`
- Success: `fill="#F5FFFC" stroke="#02C39A"`

## Sketch pill / badge

```xml
<path d="M 0 6 L 118 4 L 120 28 L 2 30 Z"
      fill="#E8FBF6" stroke="#02C39A" stroke-width="1.8" stroke-linecap="round"/>
<text x="60" y="22" font-family="Arial, sans-serif" font-size="13" font-weight="bold"
      fill="#028090" text-anchor="middle">BEFORE</text>
```

## Hub ellipse (fusion / adapter)

```xml
<ellipse cx="150" cy="150" rx="138" ry="134"
         fill="#F5FFFC" stroke="#028090" stroke-width="2.5" stroke-linecap="round"/>
<ellipse cx="150" cy="150" rx="88" ry="86"
         fill="none" stroke="#02C39A" stroke-width="2" stroke-dasharray="6 5"/>
```

## Sketch arrow

```xml
<path d="M 0 4 C 36 0 72 -2 108 4" fill="none" stroke="#028090"
      stroke-width="2.8" stroke-linecap="round"/>
<path d="M 108 4 L 92 -6 L 94 14 Z" fill="#028090"/>
```

Dashed reference line:

```xml
<path d="M 140 88 C 400 84 800 92 1004 88" fill="none" stroke="#028090"
      stroke-width="3" stroke-linecap="round" stroke-dasharray="8 6"/>
```

## IDE / terminal window (minimal)

```xml
<path d="M 6 4 L 720 6 L 722 360 L 4 358 Z" fill="#FAFAFA" stroke="#232F3E"
      stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="28" cy="32" r="6" fill="#EF5350"/>
<circle cx="48" cy="32" r="6" fill="#FFB84D"/>
<circle cx="68" cy="32" r="6" fill="#02C39A"/>
<text x="360" y="38" font-family="Arial, sans-serif" font-size="14"
      fill="#607D8B" text-anchor="middle">terminal</text>
```

## Lucide icon in defs

From [lucide.dev](https://lucide.dev/icons/) — normalize to 24×24, stroke only:

```xml
<g id="lucide-brain">
  <path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"
        fill="none" stroke="#02C39A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"
        fill="none" stroke="#02C39A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</g>
<!-- placement -->
<use href="#lucide-brain" x="28" y="28" width="32" height="32"/>
```

## Domain icons (K8s)

```xml
<g id="icon-pod">
  <polygon points="12,2 20.66,7 20.66,17 12,22 3.34,17 3.34,7"
           fill="none" stroke="#028090" stroke-width="1.8"/>
</g>
```

## Animation groups (PowerPoint)

Wrap each reveal step:

```xml
<g id="anim-step-3" transform="translate(498,28)">
  <!-- one pipeline node -->
</g>
```

Naming conventions:
- Title: `anim-titlebar`
- Comparison cards: `anim-card-{name}`
- Pipeline: `anim-step-1` … `anim-step-N`
- Fusion: `anim-input-*`, `anim-reactor`, `anim-output`
- Before/after: `anim-terminal`, `anim-report`, `anim-question`

## Safe zone

Keep all visible content inside:
- `x`: 80–1200
- `y`: 100–660 (title block may start at y=88)
- **24px** minimum gap between siblings

## Preview render

```bash
rsvg-convert -w 1280 -h 720 "sections/05-llm-agent-langchain/slides/slide1_goal.svg" \
  -o "sections/05-llm-agent-langchain/slides/.qa/slide1_goal.png"
```

Inspect PNG for clutter, contrast, and readable labels at a glance.

## File naming

```text
sections/{NN}-{section-name}/slides/slide{N}_{topic}.svg
sections/{NN}-{section-name}/slides/presentation_guide.md
```

Redo in place. New filenames only with user approval.
