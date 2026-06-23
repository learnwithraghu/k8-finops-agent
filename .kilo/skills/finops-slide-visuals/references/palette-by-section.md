# Palette by Section

Use the palette that matches the section era. **New and reworked slides default to Teal Trust on white.**

## Teal Trust (Section 05+)

Default for LLM agent, issue tracker integration, and later sections.

| Token | Hex | Use |
|-------|-----|-----|
| Slide bg | `#FFFFFF` | Full canvas |
| Charcoal | `#232F3E` | Titles, pencil strokes |
| Muted | `#607D8B` | One subtitle |
| Primary teal | `#028090` | Flow, icons, arrows |
| Seafoam | `#00A896` | Secondary |
| Mint | `#02C39A` | Success, LLM, winner |
| Warm | `#FFB84D` | YAML / policy |
| Warning | `#EF5350` | Violations |
| Card fill | `#FAFAFA` | Neutral panels |

**Do not use** dark stage palette (`#0B1020`, `#111827`, glowing orbs) in new Section 05+ work.

## AWS / GCP legacy (Sections 01–04)

Existing slides may use white cards with colored headers:

| Token | Hex | Use |
|-------|-----|-----|
| Slide bg | `#FFFFFF` | Canvas |
| Charcoal | `#232F3E` / `#37474F` | Text |
| GCP Blue | `#4285F4` | K8s / primary actions |
| AWS Orange | `#FF9900` | Python agent / connectors |
| GCP Green | `#34A853` | JSON / success output |
| Warning | `#EF5350` | Violations |
| Card fill | `#F8F9FA` | Panels |

When **reworking** legacy slides, prefer migrating to Teal Trust + pencil sketch if the section is part of the LLM/FinOps decision arc (04+). Keep AWS/GCP colors only when the slide is explicitly about cloud branding from early sections.

## Before / after accent pairing

| State | Panel tint | Border | Badge |
|-------|------------|--------|-------|
| Before (raw scan) | `#FFF8F8` | `#EF5350` | red pill |
| After (LLM report) | `#F5FFFC` | `#02C39A` | mint pill |
| Neutral fact | `#FAFAFA` | `#232F3E` | none |
| Policy | `#FFFBF2` | `#FFB84D` | none |
| Winner | `#F5FFFC` | `#02C39A` | mint banner |

## Icon stroke colors

Match icon stroke to semantic role, not random color per slide:
- K8s / scan / flow: `#028090`
- LLM / success / adapter: `#02C39A`
- Policy / YAML: `#FFB84D`
- Failure / X / alert: `#EF5350`
- Muted cloud (losers): `#607D8B`
