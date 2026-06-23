# Visual Types — FinOps Slides

Choose the slide type that matches the narration beat. Default: **one type per slide**, not a collage.

## Split metaphor (problem → gap)

**Use when:**
- section introduces a tension (data without decisions, parser bottleneck)
- left side = what we have; right side = what fails

**Examples:**
- K8s facts → manual parser failures (`slide1_goal.svg`)
- raw scan output → missing routing/draft (`slide8a_raw_scan.svg`)

**Format:** two hand-drawn panels + one arrow; 3 bullets max per side.

**Anim groups:** `anim-data-card`, `anim-parser-card`, `anim-arrow`, `anim-brain-cta`

## Fusion flow (many inputs → one reactor → output)

**Use when:**
- prompt template blends system role, YAML policy, and resource facts
- multiple inputs must feel like one decision request

**Examples:** `slide6_fusion.svg`

**Format:** 3 input cards left, hub center, output card right; 3 converging arrows max.

**Anim groups:** `anim-input-*`, `anim-reactor`, `anim-output`

## Harness / vendor comparison

**Use when:**
- choosing between cloud SDKs and LangChain
- one option is the recommended winner

**Examples:** `slide2_frameworks.svg`

**Format:** 3 small loser cards + 1 larger winner card; checkmarks on winner only.

**Anim groups:** `anim-card-aws`, `anim-card-azure`, `anim-card-gcp`, `anim-card-langchain`

## Hub + pillars

**Use when:**
- listing 3–4 capabilities around a central concept
- each pillar is a short label, not a paragraph

**Examples:** `slide3_langchain_features.svg`

**Format:** center hub ellipse + 4 side pills; no connector lines required.

**Anim groups:** `anim-hub`, `anim-pillar-1` … `anim-pillar-4`

## Workspace map

**Use when:**
- walking the repo file layout before a live demo
- files have one job each

**Examples:** `slide4_file_structure.svg`

**Format:** IDE window with **flat file list** (no tree lines) + 2–3 side callouts.

**Anim groups:** `anim-explorer`, `anim-callout-policy`, `anim-callout-agent`, `anim-callout-env`

## Pipeline rail

**Use when:**
- `main.py` chain: scan → prompt → llm → parser → report
- steps are sequential

**Examples:** `slide7_pydantic.svg`

**Format:** horizontal dashed rail + 5 icon circles; label under each node only.

**Anim groups:** `anim-step-1` … `anim-step-5`

## Adapter / provider switch

**Use when:**
- `.env` drives `ChatOpenAI` + `base_url`
- same code, different endpoints

**Examples:** `slide5_adapter.svg`

**Format:** env window, center hub, 3 provider pills, minimal arrows.

**Anim groups:** `anim-env-window`, `anim-adapter-hub`, `anim-provider-1` … `anim-provider-3`

## Before / after report

**Use when:**
- contrasting Section N output with Section N+1 output
- same resource name anchors the transition

**Examples:** `slide8a_raw_scan.svg` → `slide8b_llm_report.svg`

**Format:** before = terminal violations; after = decision card + Section handoff question.

**Anim groups:** `anim-terminal` / `anim-report`, `anim-question`

## Decision guide

```
Is there a tension between what we collect and what we decide?
  → Split metaphor

Does the section fuse policy + facts into one LLM call?
  → Fusion flow

Are we picking a framework or provider?
  → Comparison or adapter

Are we showing repo layout or pipeline order?
  → Workspace map or pipeline rail

Are we contrasting old output vs new output?
  → Before / after
```

## What not to illustrate

- Full microservice architecture the section does not implement
- Every file mentioned in `guide.md` on one slide
- JSON payloads with 10+ fields visible
- Charts with invented savings percentages
- Dark cinematic backgrounds for "premium feel"

## Slide count guidance

| Section teaching block | Typical slides |
|------------------------|----------------|
| Concept + why upgrade | 1–2 |
| Framework choice | 1 |
| Workspace + pipeline | 2 |
| Config / adapter | 1 |
| Before / after demo | 2 |

When unsure, **simplify one existing slide** rather than add a new file.
