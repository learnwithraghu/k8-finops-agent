# Guide 5: Trainer Notes — `code/query_agent.py`

**Time Budget:** 4–5 mins

**Narrative:** The smallest possible agent script — one prompt constant, one call to `run_agent`. The LLM picks MCP tools and writes a plain-English answer.

**Prerequisites:** [`4_guide.md`](4_guide.md) — `validate_mcp.py` passed; MCP container running; virtualenv activated.

---

Open the file:

```bash
cat sections/06-mcp-data-agent/code/query_agent.py
```

---

## Block 1 — Module docstring (line 1)

```python
"""Prompt -> LangChain agent -> MCP tools -> plain-text answer."""
```

**Highlight:** The four-step flow in one line — this is the Section 06 learning goal.

---

## Block 2 — Imports (lines 2–4)

```python
import asyncio

from mcp_client import run_agent
```

**Highlight:** The entire agent loop lives in `mcp_client.py`. This script only supplies a prompt.

> *Talking point: "We kept this deliberately thin so students can see the hard part lives in one place — it's shared, not repeated in every script."*

---

## Block 3 — The prompt (line 6)

```python
PROMPT = "list all namespaces"
```

**Highlight:** The only thing you change for a different question. Fixed demo string for the first run.

> *Talking point: "You give it one string, and the LLM figures out which MCP tool to call and what arguments to pass."*

---

## Block 4 — `main` (lines 9–10)

```python
async def main() -> None:
    print(await run_agent(PROMPT))
```

**Highlight:** `run_agent` handles connect → ReAct loop → cleanup → final answer. This script just prints it.

---

## Block 5 — Entry point (lines 13–14)

```python
if __name__ == "__main__":
    asyncio.run(main())
```

**Highlight:** Same async pattern as `validate_mcp.py`.

---

## Run it — default prompt

```bash
source .venv/bin/activate
python3 sections/06-mcp-data-agent/code/validate_mcp.py
python3 sections/06-mcp-data-agent/code/query_agent.py
```

**What it does:** LangChain ReAct agent picks `kubectl_get` through MCP, then prints a short plain-English summary.

---

## Expected output (default prompt)

```text
The cluster has the following namespaces: airline, booking-api, default,
flight-search, inventory, kube-node-lease, kube-public, kube-system, and payment.
```

**How to read the logs:**

| What you see | Meaning |
|--------------|---------|
| A few sentences listing namespaces | LLM received MCP data and summarized it |
| Airline namespaces named (`booking-api`, `flight-search`, etc.) | Real cluster data — not hallucinated |
| LangChain debug / tool-call traces (if logging enabled) | Agent chose `kubectl_get` with namespace-related args |
| `Connection refused` or MCP errors | Container stopped — restart from `2_guide.md` |
| OpenAI / API errors | Check `grep OPENAI .env` — LLM endpoint is separate from MCP |

Spot-check against kubectl:

```bash
kubectl get ns
```

> *Talking point: "The LLM is summarizing real cluster data here — MCP is the source of truth, not the model's memory."*

---

## Change the prompt — `kube-system` demo

Show how easy it is to ask a different question. Edit line 6 in `query_agent.py`:

```python
PROMPT = "how many pods are running in kube-system?"
```

Save and run again:

```bash
python3 sections/06-mcp-data-agent/code/query_agent.py
```

**What it does:** Same script, same `run_agent` wiring — only the prompt changed. The LLM should call `kubectl_get` for pods in `kube-system` and count them.

**Expected output (kube-system prompt):**

```text
There are N pods running in the kube-system namespace: <pod-1>, <pod-2>, ...
```

Verify:

```bash
kubectl get pods -n kube-system
```

> *Talking point: "Change one line and you get a completely different question — that's the agent pattern: prompt in, MCP out, answer back."*

Other prompts to try live:

- `"what deployments exist in booking-api?"`
- `"list configmaps in the payment namespace"`

---

**Next:** Walk through the inventory agent → `6_guide.md`
