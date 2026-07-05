# Facilitator Guide — FinOps Journey

Interactive module: [`finops-game-1.html`](finops-game-1.html)

A real-world scenario: VP Finance email about $52K unallocated spend on **NovaCart**'s prod cluster. Students navigate **Inform → Optimize → Operate** via an interactive K8 architecture map.

## How it works

| Phase | Student action | FinOps concept |
|-------|----------------|----------------|
| **Inform** | Click pulsing resources on the namespace map, inspect labels, log findings | Visibility before action |
| **Optimize** | Apply fixes to logged findings; watch unallocated $ drop | Informed trade-offs, not blanket cuts |
| **Operate** | Click through policy → scan → ticket → repeat loop | Institutionalize the monthly rhythm |

## Workshop (~15 min)

1. **2 min** — Read the CFO email on the intro screen together
2. **5 min** — Inform phase: students inspect map, log 4+ findings
3. **4 min** — Optimize: apply all fixes, discuss why FinOps ≠ "cut everything"
4. **3 min** — Operate: wire the cycle; connect to the agent they will build
5. **1 min** — Debrief, hand off to kubectl demos in the guides

## Discussion prompts

- **Inform:** "Which finding would you escalate first — missing owner or orphaned PVC?"
- **Optimize:** "Why didn't we touch inventory-service?"
- **Operate:** "What breaks if you skip Operate and only firefight monthly?"

## After the journey

1. [`1_guide.md`](../1_guide.md) — kubectl: untagged resources
2. [`2_guide.md`](../2_guide.md) — orphaned PVCs
3. [`3_guide.md`](../3_guide.md) — ownership gaps
