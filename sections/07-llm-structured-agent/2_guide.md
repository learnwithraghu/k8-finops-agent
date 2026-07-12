# Video 2: Walk the Rules File

**Transcript:** [`transcript/2.md`](transcript/2.md)

**Time Budget:** 3–4 min
**Format:** Talking head / diagram (no live terminal)
**Prerequisites:** [`1_guide.md`](1_guide.md) — understand why policy from file matters

---

## Key takeaways

- `config/tagging-rules.yaml` is loaded from file at runtime — not pasted into the prompt
- `required_tags`, `label_mappings`, and `excluded_namespaces` define the audit standard
- `run_agent` attaches the rules as a separate system message before the instruction prompt

## Demo handoff

No hands-on steps in this video. The live build starts in `3_guide.md` — walk through `structured_auditor.py` block by block.
