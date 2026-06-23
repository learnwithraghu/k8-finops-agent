# QA Checklist — FinOps Slide SVGs

Run after each slide edit. Simplify or redraw if any critical check fails.

## Brand fit

- [ ] White canvas `#FFFFFF` (Section 05+)
- [ ] Pencil-sketch hand-drawn panels, not dark SaaS dashboard
- [ ] Teal Trust accents sparingly — not neon AI marketing
- [ ] Teaching clarity over cinematic "premium dark stage"
- [ ] Matches gold references in `sections/05-llm-agent-langchain/slides/`

## Narrative accuracy

- [ ] Slide matches `presentation_guide.md` narration beat
- [ ] Labels use real file names, classes, and terms from section code
- [ ] Does not oversimplify or contradict `guide.md`
- [ ] Before/after pair shares the same resource anchor when applicable

## Composition

- [ ] One clear idea per slide
- [ ] Hero focal region ~35–45% of canvas
- [ ] Generous whitespace; not edge-to-edge cards
- [ ] ≤40 visible words on slide face
- [ ] Layout type varies from previous slide in the deck (not 5 identical grids)

## Lines and clutter

- [ ] No tree connector spaghetti for simple file lists
- [ ] ≤3 primary flow arrows; none crossing
- [ ] No duplicate shadow layers under panels
- [ ] No decorative background circles or gradients
- [ ] No filters, masks, or clippath

## Labels and type

- [ ] Title ~40px + one subtitle line only
- [ ] Arial for PPT; Courier only for paths/terminal
- [ ] 4–6 short labels max on diagram body
- [ ] No redundant bottom banner repeating the subtitle

## PPT / technical

- [ ] `viewBox="0 0 1280 720"` + `width="100%"` `height="100%"`
- [ ] Icons in `<defs>` with `<use href="#...">`
- [ ] Animatable units in `<g id="anim-*">`
- [ ] Content in safe zone `x=80..1200, y=100..660`
- [ ] Min 24px gap between siblings
- [ ] Redo in place — no unapproved new slide files

## Data honesty

- [ ] No invented cost savings or metric charts
- [ ] Terminal snippets reflect plausible section output
- [ ] Qualitative comparisons only unless sourced from code/demo

## File and wiring

- [ ] SVG saved under `sections/{NN}-{section}/slides/`
- [ ] `presentation_guide.md` updated if order, title, or anim notes changed
- [ ] Optional `.qa/*.png` preview generated for visual scan

## Severity guide

| Issue | Action |
|-------|--------|
| Dark stage / corporate infographic look | Redraw to white pencil sketch |
| Too many lines, text, or cards | Remove elements first |
| Crossing arrows | Reroute or drop arrows |
| Wrong file/class name | Fix label |
| PPT-unsafe filters | Remove and use flat fills |
| Slide fine but busy | Drop one panel or callout |

## Final litmus test

Ask:
- Does this land in 2 seconds at projector distance?
- Is it lighter than reading the narration bullets aloud?
- Would a K8s FinOps learner nod, not squint?

If yes to all three, ship it.
