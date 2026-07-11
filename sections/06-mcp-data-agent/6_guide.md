# Guide 6: Trainer Notes — `code/snapshot_collector.py`

**Time Budget:** 4–5 mins

**Narrative:** Same agent path as the query script, but a broader inventory prompt and a higher token limit. The LLM gathers cluster data through MCP and writes a FinOps-oriented summary.

**Prerequisites:** [`5_guide.md`](5_guide.md) — query agent working; MCP container running; virtualenv activated.

---

Open the file:

```bash
cat sections/06-mcp-data-agent/code/snapshot_collector.py
```

---

## Block 1 — Module docstring (line 1)

```python
"""Ask a LangChain agent to inspect the cluster and print its final answer."""
```

**Highlight:** Still agent-driven — not a deterministic JSON collector. The LLM chooses tool calls and writes the final output.

---

## Block 2 — Imports (lines 2–4)

```python
import asyncio

from mcp_client import run_agent
```

**Highlight:** Identical import pattern to `query_agent.py` — shared plumbing, different prompt.

---

## Block 3 — The inventory prompt (lines 6–17)

```python
PROMPT = """
You are collecting a Kubernetes FinOps inventory through MCP tools.

Use the available Kubernetes MCP tools to:
1. List all namespaces.
2. Fetch deployments, pods, services, persistent volume claims, and configmaps across all namespaces.
3. Ignore kube-* namespaces and local-path-storage when summarizing application resources.
4. Summarize the inventory in plain English.

Include resource names, namespaces, kinds, and labels when labels are present.
Use only data returned by the tools. Do not invent resources.
"""
```

**Highlight:** Multi-step instructions in natural language. The LLM plans multiple `kubectl_get` calls instead of one.

> *Talking point: "Same `run_agent` function — we just gave it a bigger prompt. That's how you go from a one-liner question to a full FinOps inventory task."*

Key lines to call out:

| Line | Why highlight |
|------|---------------|
| `List all namespaces` | First tool call the agent should make |
| `deployments, pods, services...` | Tells the LLM which resource types to fetch |
| `Ignore kube-* namespaces` | Keeps the summary focused on application workloads |
| `labels when labels are present` | Sets up Section 07 — labels matter for FinOps |
| `Do not invent resources` | Grounds the LLM in MCP data only |

---

## Block 4 — `main` with higher token limit (lines 20–21)

```python
async def main() -> None:
    print(await run_agent(PROMPT, max_tokens=2048))
```

**Highlight:** `max_tokens=2048` — inventory summaries are longer than a namespace list. Passed through to `build_llm` in `mcp_client.py`.

> *Talking point: "The default is 512 tokens from `.env`, but an inventory summary needs more room for namespaces, kinds, and labels."*

---

## Block 5 — Entry point (lines 24–25)

```python
if __name__ == "__main__":
    asyncio.run(main())
```

**Highlight:** Same entry pattern as the other scripts.

---

## Run it

```bash
source .venv/bin/activate
python3 sections/06-mcp-data-agent/code/validate_mcp.py
python3 sections/06-mcp-data-agent/code/snapshot_collector.py
```

**What it does:** LangChain agent makes multiple MCP tool calls, then prints a plain-English inventory summary. This may take 30–60 seconds — the LLM is fetching several resource types.

---

## Expected output

A multi-paragraph or markdown-style summary, for example:

```text
## Cluster Inventory Summary

### Application Namespaces
- **booking-api**: Deployment `booking-api` (1/1 ready), Pod `booking-api-...`, Service `booking-api`, PVC `booking-api-data` (Pending), ConfigMap `booking-api-config`
- **flight-search**: Deployment `flight-search` (1/1 ready), ...
- **inventory**: ...
- **payment**: ...

### Labels observed
- `app=booking-api` on booking-api deployment and pods
- ...

### Notes
- Several PVCs are in Pending state (no storage class bound)
- kube-system and kube-public resources excluded per instructions
```

**How to read the logs:**

| What you see | Meaning |
|--------------|---------|
| Multiple paragraphs grouped by namespace | LLM followed the inventory prompt structure |
| Resource names matching `kubectl get` output | Data came from MCP, not invented |
| Labels listed when present | MCP `kubectl_get` responses included label metadata |
| `kube-*` namespaces omitted | LLM respected the ignore instruction |
| Truncated output | Increase `max_tokens` or shorten the prompt |
| Missing resource types | Re-run — LLM tool choice can vary; spot-check with kubectl below |

Spot-check against kubectl:

```bash
kubectl get deploy,pod,svc,pvc,configmap -A
```

> *Talking point: "For now we just print what the LLM comes back with. Section 07 builds on this — structured JSON, tagging rules, and policy scoring."*

---

**Next:** Add policy and structured output → `sections/07-llm-structured-agent`
