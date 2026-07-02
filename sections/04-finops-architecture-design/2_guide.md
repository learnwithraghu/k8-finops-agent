# Video: The Architecture Pattern

**GSheet concepts:** 040-000 Architecture pattern
**Expanded concepts:** Build vs buy, standard interfaces, deterministic vs reasoning layers
**Time Budget:** 3 min
**Format:** Whiteboard / talking head
**Prerequisites:** The problem we're solving

---

## Transcript

### Opening

We named gather, analyze, act. Now choose **how** each stage runs — by articulating trade-offs any architect should defend in a design review.

---

### Gather: three approaches

**Manual inspection** — fine for learning, poor as a scheduled habit.

**Custom collectors** — full control, full maintenance burden as APIs and resource types evolve.

**Standard read interface** — shared protocol any client can use; prebuilt readers reduce bespoke code; dependency on an external component you do not own.

For teaching and for many teams, the third option wins on time-to-trust: prove reading works, then build upward.

Draw: platform → reader → inventory.

---

### Analyze: rules vs reasoning

**Deterministic rules** — excellent for simple predicates, brittle for relational judgment across objects.

**Model-assisted analysis** — applies human-edited policy with context; needs structured output constraints so results are reviewable.

Policy changes frequently in FinOps. Favor an analyze stage that updates when standards documents update.

Draw: inventory + policy → findings.

---

### Act: reports vs boards

Archives are good for history. **Boards** — tasks with status and owners — are how Operate happens. Findings should land where sprint planning already lives.

Draw: findings → tasks → closed work.

---

### Close

Full line: platform → inventory → findings → tasks. Next video assigns responsibilities and boundaries to each box.

---

## Key takeaways
- Gather favors maintainable read paths over one-off scripts
- Analyze favors policy-driven reasoning with structured, reviewable output
- Act requires trackable tasks, not static exports
- The pipeline is linear and stage-isolated by design

## Demo handoff

Upcoming work validates gather first, then builds analyze and act — never skipping proof at the bottom of the stack.
