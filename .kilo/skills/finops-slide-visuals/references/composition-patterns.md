# Composition Patterns — FinOps Slides

Invent layouts from the **section narrative**, not from generic AI clipart. Reuse *patterns*, not identical scenes across sections.

## Metaphor invention (3 steps)

### 1. Name the FinOps concept

Examples from this repo:
- data without decisions
- parser brittleness / alias mismatch
- prompt beats parsers
- harness lock-in
- orphan PVC / missing owner tag
- unactioned scan output
- adapter via `base_url`

### 2. Map to an operational image

| Concept | Visual mapping |
|---------|----------------|
| rich facts, no decision | full inbox → empty verdict |
| parser brittleness | checklist with red X marks |
| prompt fusion | three streams into one hub |
| vendor lock-in | three cloud cards, one open chain link winner |
| pipeline | scan → fuse → infer → type → report |
| raw scan | terminal VIOLATION lines |
| LLM report | decision card + issue draft |
| tracking gap | question mark → Section 06 |

### 3. Pick 1 hero + ≤4 support regions

Hero occupies **35–45%** of slide area. Supporting labels sit in side rails or small pills — they do not compete with the hero.

**FinOps object pool** (rotate across slides):
- K8s hexagon pod, YAML doc, terminal window, `.env` key
- Lucide: brain, link, cloud, braces, clipboard, sparkles
- Policy tint panel (warm), failure tint panel (red), success tint (mint)

Avoid stacking more than **two metaphor object types** per slide.

## Layout patterns

### Split problem / gap

Left: what works (facts collected). Right: what breaks (parser limits). One arrow between.

Good for: Section 04 → 05 handoff, `slide1_goal.svg`.

### Fusion reactor

Three inputs converge on a labeled hub (`PROMPT_TEMPLATE`, `ChatOpenAI`, adapter). One output card.

Good for: policy + facts + role, `slide6_fusion.svg`.

### Shootout row

Three muted options + one highlighted winner card with badge.

Good for: LangChain vs cloud SDKs, `slide2_frameworks.svg`.

### Center hub + pillars

Ellipse hub in center; 2–4 labeled pills on sides. **No lines** unless essential.

Good for: four LangChain pillars, `slide3_langchain_features.svg`.

### Flat explorer + callouts

Single IDE frame; files as a **vertical list** with icons. Right column: 2–3 callout pills max.

Good for: workspace walkthrough, `slide4_file_structure.svg`.

### Step rail

One container; dashed horizontal path; 5 nodes with icon + one-word label.

Good for: agent pipeline, `slide7_pydantic.svg`.

### Env → hub → providers

`.env` window, center adapter ellipse, stacked provider pills. **≤3 arrows**.

Good for: model/provider choice, `slide5_adapter.svg`.

### Before / after pair

Slide A: sparse terminal, red accent, "BEFORE" pill. Slide B: decision report, mint accent, "AFTER" pill. **Same resource name** on both.

Good for: scan vs LLM report, `slide8a` / `slide8b`.

## Label guidance

Labels name the *artifact*, not the whole lesson:
- `tagging-rules.yaml` not "corporate policy configuration file"
- `K8sScanner` not "kubernetes metadata collection subsystem"
- `upgrade the brain` not "implement large language model based decision engine"

Max **6 short labels** on slide face. Title + subtitle are separate.

## Whitespace rules

- Title block: top ~140px only.
- Focal content: `y=180..580`.
- Bottom tagline optional; one line max.
- Minimum **24px** gap between sibling panels.

## Anti-patterns

- Dark stage with glowing circles (deprecated in Section 05+)
- Offset shadow cards (`rect` at `x+12, y+12` under every panel)
- File tree with 10+ connector lines
- 5+ curved arrows crossing the canvas
- Winner card + bottom banner + side callouts all repeating the same sentence
- Before/after slides that look identical except text color

## Originality rule

Each section deck should **vary layout type** across slides. If three slides in a row use the same card grid, change the next one to hub, rail, or split pattern.

Gold reference deck: `sections/05-llm-agent-langchain/slides/`.
