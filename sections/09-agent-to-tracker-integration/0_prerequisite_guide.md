# Instructor Prerequisite: Services & API Key

**Audience:** Instructor only — run this before `1_guide.md`. Do not walk students through service startup during the live demo.

**Time Budget:** 2–3 mins

---

## Before you start

Confirm Supergateway (Section 05) is running:

```bash
curl -s http://localhost:8000/healthz
```

**What it does:** Checks the MCP endpoint is alive. Should return `ok`.

---

Confirm the Issue Tracker (Section 08) is running:

```bash
curl -s http://localhost:8085/docs | head -5
```

**What it does:** Checks the tracker REST API is responding. If this fails, restart the tracker.

> *If tracker is not running:*
> ```bash
> docker run --rm -p 8085:8000 -p 8086:8001 --name finops-issue-tracker finops-issue-tracker:latest &
> ```

---

Confirm API key is set:

```bash
test -n "$OPENAI_API_KEY" && echo "API key is set" || echo "OPENAI_API_KEY is not set"
```

**What it does:** Checks that the OpenAI API key is present. The agent needs this for LLM analysis.

---

## 1) Inspect the agent code

```bash
cat sections/09-agent-to-tracker-integration/agent.py
```

**What it does:** Shows the full agent — collection (MCP), analysis (LLM), and integration (tracker MCP). Three phases in one file.

> *Talking point: "This is the monolith. Section 10 refactors it. For now, notice the three phases: collect, analyze, post."*

---

## 2) Ready to teach

When all services are running, start the live walkthrough with:

- `1_guide.md` — Run the full agent
- `2_guide.md` — Verify the automation

## Cleanup after the session

```bash
docker stop finops-issue-tracker
```
