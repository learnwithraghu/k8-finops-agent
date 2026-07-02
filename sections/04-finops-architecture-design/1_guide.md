# Video: The Problem We're Solving

**GSheet concepts:** 040-000 Converting problem statement to code design
**Expanded concepts:** Organizational cost of manual governance, system design before implementation
**Time Budget:** 3 min
**Format:** Whiteboard / talking head
**Prerequisites:** Ownership gaps at scale

---

## Transcript

### Opening

You have felt SkyLine Air's pain manually: untagged workloads, idle storage, findings with no owner. This module designs the system that replaces heroic inspection with a repeatable pipeline.

No implementation yet — only architecture.

---

### Recap the failure modes

Technical outages recover with the right operational change. Organizational outages recover only when **metadata and process** exist — owners, cost centers, trackable remediation.

Manual walks work on a laptop. They fail at production scale. The design question is:

How do we move from a live platform to actionable governance findings **automatically**?

---

### Three movements

**Gather** platform state into neutral inventory.

**Analyze** inventory against written policy to produce structured findings.

**Act** by creating trackable tasks teams close.

That sequence mirrors Inform, Optimize, and Operate. Each stage has one job. Mixed responsibilities make debugging painful.

> *Talking point: "Design the line before you hire the workers."*

---

### Close

Next video compares approaches for each movement — trade-offs, not brand names as instructions.

---

## Key takeaways
- Organizational governance failures need system design, not more manual grep
- Gather → analyze → act is the core pipeline
- Whiteboard clarity precedes implementation in this course

## Demo handoff

This module has no hands-on build. Demos resume once each pipeline stage is defined and then implemented.
