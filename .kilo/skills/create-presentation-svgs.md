# K8s FinOps Agent - Skill for Creating Presentation SVGs

## Purpose

This skill provides the design guidelines, code structure, and checklist for creating and refining visually stunning, high-quality SVG slide graphics for presentation decks (PowerPoint, Keynote, Google Slides).

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
Use a clean, modern color scheme (e.g., AWS/GCP style colors):
- **Base Text / Charcoal**: `#232F3E` (AWS Charcoal) or `#37474F` (GCP Slate)
- **Primary / Action Blue**: `#4285F4` (GCP Blue) or `#1E88E5`
- **Exclusion / Config Orange**: `#FF9900` (AWS Orange) or `#B78103`
- **Success / Compliance Green**: `#34A853` (GCP Green) or `#2E7D32`
- **Warning / Non-compliance Red**: `#EF5350` or `#C62828`
- **Card Backgrounds**: Light neutral tints like `#F8F9FA` or `#ECEFF1`

### Step 3: Leverage Reusable Icon Definitions
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

### Step 4: Keep Connections & Lines Clean ("No Spaghetti")
- **Avoid Crossing Lines**: Prevent lines from intersecting. Instead of drawing a complex maze of connections, align components vertically or horizontally and use straight or clear curved lines.
- **Dashed vs. Solid**: Use solid lines for primary active routing (e.g. data pipelines) and dashed lines for logic references or validations.
- **Arrows**: Add small polygons as arrowheads at the ends of connection paths for clear flow direction.

### Step 5: Code Annotations & Diagnostic Callouts
When showing file contents or JSON snippets (e.g., metadata structures):
- Display the snippet in a stylized IDE window container (complete with browser control dots).
- Draw highlighting rects over key properties.
- Connect highlighted properties directly to colored inspector/diagnostic cards using dotted lines to immediately explain the business logic associated with the property.

---

## Checklist

- [ ] Does the SVG use the `viewBox="0 0 1280 720"` standard?
- [ ] Is the typography consistent (using `Arial` or system-ui sans-serif fonts)?
- [ ] Are all fonts set with absolute sizes to avoid scaling rendering issues?
- [ ] Are vector icons defined in `<defs>` and reused with `<use>`?
- [ ] Are connections straight, parallel, or neatly curved (no intersecting lines)?
- [ ] Is there sufficient margins (headers at X=80, slides bounded inside Y=640)?
- [ ] Does the SVG scale responsively inside PPT via `width="100%"` and `height="100%"`?
