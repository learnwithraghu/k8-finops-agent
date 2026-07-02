# Video: Component Design and Trade-offs

**GSheet concepts:** 050-000 Designing the FinOps Agent key building blocks
**Expanded concepts:** Single responsibility, teachability vs production fidelity
**Time Budget:** 3 min
**Format:** Whiteboard / talking head
**Prerequisites:** Architecture pattern

---

## Transcript

### Opening

The pipeline is drawn. This video gives each component a job description — inputs, outputs, and what we simplify on purpose for learning.

---

### Reader component

Exposes platform state through a stable interface. Input: questions about what exists. Output: structured inventory.

Prefer a maintained reader over writing your own API glue unless you have unusual constraints. Prove connectivity early with a minimal smoke test.

---

### Collector component

Orchestrates reader calls into one inventory snapshot. No policy. No severity. Deterministic for a given platform state — essential for debugging.

If findings look wrong later, you ask: was inventory wrong, or was analysis wrong?

---

### Analyzer component

Consumes inventory plus policy standards. Produces structured findings — title, location, severity, suggested owner, short reasoning.

Reasoning handles cases rules mishandle: cross-object relationships, ambiguous legacy assets. Output must match a fixed schema so invalid results fail before reaching users.

---

### Tracker component

Accepts findings and exposes tasks on a board. Teaching uses a lightweight local service; production might use enterprise issue tracking. Integration shape stays the same: structured finding in, assigned task out.

---

### Integration

Short orchestration wiring the three movements in order. One run, visible tasks at the end.

### Close

Next we implement gather — proving the reader before any agent code.

---

## Key takeaways
- Each component has one responsibility and clear handoffs
- Separation enables stage-level testing and replacement
- Teaching components favor clarity; integration patterns transfer to production tools

## Demo handoff

Implementation proceeds reader → collector → analyzer → tracker, validating each handoff before the full run.
