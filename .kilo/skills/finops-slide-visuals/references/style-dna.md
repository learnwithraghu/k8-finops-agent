# Style DNA — K8s FinOps Agent Slides

## One line

A platform engineer whiteboarding a FinOps decision on a clean slide — clear, technical, not corporate.

Like someone explaining why the parser failed and the LLM path wins, sketched in pencil on a blank deck page.

## Must have

- **16:9** canvas: `viewBox="0 0 1280 720"`.
- **Pure white background** `#FFFFFF` for Section 05+ decks.
- **Pencil-sketch outlines**: slightly irregular `<path>` corners, `stroke-linecap="round"`, `stroke-linejoin="round"`, stroke width ~2–2.5.
- **Lots of whitespace**: focal subject ~35–45% of canvas; avoid filling the slide edge-to-edge.
- **Sparse labels**: max **40 words** visible; prefer icons + short nouns over sentences.
- **One core idea per slide**.
- **Teal Trust accents** used sparingly — not a rainbow deck.

## Color (Section 05+ default)

| Token | Hex | Use |
|-------|-----|-----|
| Slide bg | `#FFFFFF` | Full canvas |
| Charcoal | `#232F3E` | Titles, primary labels, pencil strokes |
| Muted | `#607D8B` | One subtitle line only |
| Primary teal | `#028090` | Active flow, icons, arrows |
| Seafoam | `#00A896` | Secondary highlights |
| Mint | `#02C39A` | Success, winner, LLM path |
| Warm | `#FFB84D` | Policy YAML, config emphasis |
| Warning | `#EF5350` | Violations, parser failures |
| Card fill | `#FAFAFA` | Light panels on white |
| Tint success | `#F5FFFC` | Winner / adapter panels |
| Tint warn | `#FFF8F8` | Before / failure panels |
| Tint policy | `#FFFBF2` | YAML / policy panels |

Most strokes stay charcoal or teal. Use warm/red tints only to signal policy vs failure.

## Typography

- **Arial** (or system-ui sans-serif) for PPT compatibility — not handwriting fonts.
- Title: ~40px bold charcoal at `x=80, y=88`.
- Subtitle: one line, ~20px muted at `y=128`.
- Body labels: 15–18px; monospace (`Courier New`) only for file paths and terminal snippets.
- No duplicate title bars, badges, and headings on the same slide.

## Pencil sketch technique (SVG)

1. Replace perfect `<rect rx="...">` chrome with hand-drawn `<path>` panels (corners off by 2–4px).
2. Use **light fills** (`#FAFAFA`, tinted panels) — not dark `#0B1020` stage layouts.
3. Prefer **one border per panel** — no offset shadow rects (`x+12, y+12` duplicates).
4. Arrows: single curved or straight path + small triangle head; max 3 flow lines per slide.
5. Icons: Lucide strokes in `<defs>`, placed via `<use>` — consistent 24–32px size.
6. Ellipses for hubs feel more sketch-like than nested perfect circles.

## Mood

- Teaching clarity over demo polish.
- FinOps operational reality: tags, owners, orphans, adapters, reports.
- Confident and restrained — not hype, not cute.

## Absolutely avoid

- Dark full-slide backgrounds (`#0B1020`, glowing orbs, neon rings).
- Corporate infographic grids with 8+ equal cards.
- Tree-view connector lines for simple file lists (use flat indented list).
- Spaghetti crossing arrows.
- Filters, masks, clipPath, heavy gradients (PPT breaks).
- Robot mascots, glowing brains, holographic AI stock art.
- Real app screenshots embedded in slides.
- Repeating the same card-grid layout on every slide in a section.

## Aesthetic direction

Think: **whiteboard backup slide**, **engineer notebook sketch**, **Section 05 deck**.

Not: dark keynote stage, SaaS marketing hero, LinkedIn carousel infographic.

## Section palette exceptions

Sections 01–04 may use legacy **AWS/GCP** blues and oranges on white cards. See [palette-by-section.md](palette-by-section.md). New and reworked slides in Section 05+ use **Teal Trust on white** only.
