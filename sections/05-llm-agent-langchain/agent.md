# agent.md — Section Maintenance Rules

This file tells any AI coding agent (or human contributor) what must be kept in sync
whenever code in this section is changed.

---

## What this section teaches

Section 05 teaches learners how to connect a LangChain-powered agent to an
**OpenAI-compatible LLM endpoint** and use it to turn raw Kubernetes tagging
violations into structured, decision-oriented recommendations.

The **teaching outcome** must be preserved across all code changes.

---

## Rule 1 — guide.md must always reflect the code

`guide.md` is the learner-facing guide. It is not optional documentation.
Every code change that affects **how the agent is configured or run** must be
mirrored in `guide.md` before the change is considered complete.

### What triggers a guide.md update

| Code change | Required guide.md update |
|---|---|
| LLM provider or library changes (e.g. swap `ChatOpenAI` for another) | Update Steps 2, 6, and the "What to notice" section |
| New or renamed environment variables | Update Steps 3, 4, and the example `.env` block |
| New Python dependency added/removed | Update Step 2 if it changes what the learner reads in `analyzer.py` |
| Run command changes | Update Step 6 |
| Config file location changes | Update "Where the agent code lives" |
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
- do not add AWS-specific content unless the section explicitly uses AWS services

---

## Rule 3 — section_goal.md must stay accurate

`section_goal.md` is the one-line description of what the section achieves.
Update it if the LLM provider, integration method, or learning objective changes.

---

## Rule 4 — .env.example must stay in sync with main.py

`main.py` reads from `.env`. `.env.example` is the reference for learners.
Any new `os.getenv(...)` call in `main.py` must have a corresponding entry
in `.env.example` with a safe placeholder value.

---

## Current technical state (update this when code changes)

| Item | Current value |
|---|---|
| LLM client library | `langchain-openai` (`ChatOpenAI`) |
| Endpoint base URL | `https://api.ai.kodekloud.com/v1` (set via `OPENAI_BASE_URL`) |
| Model | configurable via `OPENAI_MODEL_ID` (default: `gpt-4o`) |
| Auth | API key via `OPENAI_API_KEY` in `.env` |
| LangChain version | `langchain>=0.1.0`, `langchain-openai>=0.1.0`, `langchain-core>=0.1.0` |
| Run command | `PYTHONPATH=sections/05-bedrock-decision-flow python3 -m agent.main` |
| Key env vars | `OPENAI_BASE_URL`, `OPENAI_API_KEY`, `OPENAI_MODEL_ID`, `OPENAI_MAX_TOKENS`, `OPENAI_TEMPERATURE` |

---

## Checklist for any PR / change to this section

- [ ] `agent/analyzer.py` — if changed, Steps 2 and 7 of `guide.md` reviewed
- [ ] `agent/main.py` — if changed, Steps 3, 4, and 6 of `guide.md` reviewed
- [ ] `agent/tagging_violations.py` — if changed, Step 1 of `guide.md` reviewed
- [ ] `.env` / `.env.example` — if changed, Steps 3 and 4 of `guide.md` reviewed
- [ ] `requirements.txt` — if changed, `agent.md` "Current technical state" table updated
- [ ] `section_goal.md` — still accurate after this change?
- [ ] `guide.md` "Expected outcome" — still achievable after this change?
