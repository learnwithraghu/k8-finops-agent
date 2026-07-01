# Instructor Prerequisite: Supergateway, Python Environment & API Key

**Audience:** Instructor only — run this before `1_guide.md`. Do not walk students through pip install during the live demo.

**Time Budget:** 2–3 mins

---

## Before you start

Confirm Supergateway from Section 05 is still running:

```bash
curl -s http://localhost:8000/healthz
```

**What it does:** Checks the MCP endpoint is alive. Should return `ok`.

> *If this fails, restart Supergateway using the command in `sections/05-mcp-k8-agent/0_prerequisite_guide.md` step 3.*

---

## 1) Set up the Python environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r sections/07-llm-structured-agent/requirements.txt
```

**What it does:** Creates a virtualenv and installs LangChain, OpenAI, Pydantic, and MCP client dependencies.

---

## 2) Confirm API key is set

```bash
test -n "$OPENAI_API_KEY" && echo "API key is set" || echo "OPENAI_API_KEY is not set"
```

**What it does:** Checks that the OpenAI API key environment variable is present. The agent needs this to call the LLM.

> *If using a `.env` file, confirm it exists at the repo root: `cat .env | grep OPENAI`*

---

## 3) Inspect the agent code

```bash
cat sections/07-llm-structured-agent/agent.py
```

**What it does:** Shows the agent — it collects data via MCP (same as Section 06), then sends it to an LLM with tagging rules to produce structured findings.

> *Talking point: "We took the collection logic from Section 06 and added LangChain/OpenAI on top. Same data in, structured findings out."*

---

## 4) Inspect the tagging rules

```bash
cat sections/07-llm-structured-agent/config/tagging-rules.yaml
```

**What it does:** Shows the policy the LLM uses to judge resources. This defines required labels, ownership rules, and severity levels.

> *Talking point: "The tagging rules are the policy. The LLM applies them to the snapshot. Without rules, the LLM has no standard to check against."*

---

## 5) Ready to teach

When setup passes, start the live walkthrough with:

- `1_guide.md` — Run the structured agent
- `2_guide.md` — Audit the findings
