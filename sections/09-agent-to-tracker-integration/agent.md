# agent.md — Section 09 Maintenance Rules

This file tells any AI coding agent (or human contributor) what must be kept in sync
whenever code in this section is changed.

---

## What this section teaches

Section 09 teaches learners how to connect the **Section 07 LLM structured agent**
to the **Section 08 issue tracker service**. The only new responsibility in this
section is turning Section 07's `TicketBatch` findings into tracker tickets via
a small HTTP client.

The teaching outcome must be preserved across all code changes.

---

## Current transitional state (update when the rewrite lands)

| Item | Current (transitional) | Target (after rewrite) |
|---|---|---|
| Inputs to `main.py` | K8sScanner + OpenAI LLM | Section 07's `TicketBatch` JSON (`--findings <file>`) |
| Files in `agent/` | `scanner.py`, `analyzer.py`, `main.py`, `tracker.py` | `main.py`, `tracker.py` only |
| LLM calls | yes (via `analyzer.analyze_resource`) | none — analysis belongs to Section 07 |
| `tracker.build_payload` input | `(K8sResource, ResourceDecision)` | `TrackerTicket` (from `agent.models` or imported from Section 07) |
| Tracker endpoint | `POST /create-issue` on `ISSUE_TRACKER_URL` | unchanged |
| Run command | `PYTHONPATH=sections/09-agent-to-tracker-integration python3 -m agent.main` | `…python3 -m agent.main --findings /tmp/section07-findings.json` |

Until the rewrite lands, `scanner.py`, `analyzer.py`, and `config/tagging-rules.yaml`
are kept only to keep the transitional flow runnable. Do not invest in teaching
those files; they are slated for deletion.

---

## Rule 1 — guide.md must always reflect the code

`guide.md` is the learner-facing guide. It is not optional documentation.
Every code change that affects **how the agent is configured or run** must be
mirrored in `guide.md` before the change is considered complete.

### What triggers a guide.md update

| Code change | Required guide.md update |
|---|---|
| Rewrite of `main.py` to consume `TicketBatch` | Update Steps 1, 3, and 4 (run command) |
| Removal of `scanner.py` / `analyzer.py` | Update Steps 3, 4, and the "Discussion" block |
| New or renamed environment variables | Update Steps 1 and the example `.env` block |
| New Python dependency added/removed | Update Step 2 or 3 if it changes what the learner reads |
| Tracker payload field changes | Update Step 2 |
| New agent file added | Add a new numbered step describing what to read and why |

---

## Rule 2 — preserve the teaching style

`guide.md` uses a consistent teaching style. Do not change the format.

- Each step starts with a shell command the learner runs
- Every step has a **"What to look for"** block pointing learners at the right concept
- Steps are numbered and build on each other
- Explanations are short — the code is the primary learning material
- No step should assume knowledge from outside the section

When updating guide.md:
- match the existing tone (instructive, minimal, no filler)
- keep the "What to look for" bullets aligned with what is actually in the code
- do not reintroduce LLM analysis here — that belongs to Section 07

---

## Rule 3 — section_goal.md must stay accurate

`section_goal.md` is the one-line description of what the section achieves.
Update it when the integration method or learning objective changes.

---

## Rule 4 — .env.example must stay in sync with main.py

`main.py` reads from `.env`. `.env.example` is the reference for learners.
Any new `os.getenv(...)` call in `main.py` must have a corresponding entry
in `.env.example` with a safe placeholder value.

---

## Checklist for any PR / change to this section

- [ ] `agent/tracker.py` — if changed, Step 2 of `guide.md` reviewed
- [ ] `agent/main.py` — if changed, Steps 1, 3, and 4 of `guide.md` reviewed
- [ ] If the Section 07 → tracker rewrite lands in this change:
  - [ ] `agent/scanner.py`, `agent/analyzer.py`, `config/tagging-rules.yaml` deleted
  - [ ] Steps 3 and 4 rewritten to describe the `--findings` flow
  - [ ] `section_goal.md` "Notes on the current code" block removed
- [ ] `.env` / `.env.example` — if changed, Step 1 of `guide.md` reviewed
- [ ] `requirements.txt` — if changed, "Current transitional state" table above updated
- [ ] `section_goal.md` — still accurate after this change?
- [ ] `guide.md` "Expected outcome" — still achievable after this change?