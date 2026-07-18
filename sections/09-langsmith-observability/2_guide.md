# Video 2: LangSmith Project & `.env`

**Time Budget:** ~3 mins

**Prerequisites:** [`1_guide.md`](1_guide.md) — why tracing matters; LangSmith account ready; virtualenv activated.

> **Legend:** Blockquote lines are on-screen actions — do not read them aloud. Everything else is your script.

---

### Opening (~15 sec)

Tracing is configuration, not a rewrite. We point LangChain at LangSmith with three environment variables, then the same Section 07 auditor starts sending runs.

> **Do:** Open the repo-root `.env` and `.env.example` side by side.

---

### Step 1 — Confirm the project in LangSmith

Open [https://smith.langchain.com](https://smith.langchain.com) and select (or create) a project — for this course use `k8-finops-agent` (or the name you will put in `.env`).

**What it does:** Gives traces a home. Runs appear under this project name after the auditor runs.

> **Say:** "One project for the course. Every agent run from this repo lands here when tracing is on."

---

### Step 2 — Add LangSmith keys to `.env`

In the repo-root `.env`, add (or confirm):

```bash
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your-langsmith-api-key
LANGSMITH_PROJECT=k8-finops-agent
```

Match the values from `.env.example`. Keep your real API key out of git — only `.env.example` is committed with placeholders.

**What it does:**
1. `LANGSMITH_TRACING=true` — turn automatic LangChain tracing on
2. `LANGSMITH_API_KEY` — authenticate to LangSmith
3. `LANGSMITH_PROJECT` — which project receives the runs

> **Do:** Point at the three lines. Do not paste a real key on screen if recording.

---

### Step 3 — How the auditor picks them up

Open `sections/09-langsmith-observability/code/mcp_client.py` and find `load_dotenv`:

```python
load_dotenv(Path(__file__).parents[3] / ".env")
```

**The chain:**
1. `structured_auditor.py` imports `run_agent` from `mcp_client`
2. `mcp_client` loads the repo-root `.env` at import time
3. LangChain sees `LANGSMITH_*` and sends traces — no new Python file, no new function

> **Say:** "Same `load_dotenv` as Section 07. We only added keys to the file it already reads."

---

### Close (~10 sec)

Env is set. Next we run the copied policy auditor — same command shape as Section 07, different section path.

> **Do:** Save `.env`. Open `3_guide.md`.
