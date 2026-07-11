# Video 5: Audit Kubernetes Labels via MCP Agent

**Time Budget:** 4–5 mins

**Narrative:** Same agent path as the query script, but a label-audit prompt and a higher token limit. The LLM gathers label metadata through MCP and writes a FinOps-oriented gap report.

**Prerequisites:** [`4_guide.md`](4_guide.md) — query agent working; MCP container running; virtualenv activated.

---

Open the file:

```bash
cat sections/06-mcp-data-agent/code/label_auditor.py
```

---

## Block 1 — Module docstring (line 1)

```python
"""Ask a LangChain agent to audit cluster labels via MCP and print its final answer."""
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

## Block 3 — The label audit prompt (lines 6–17)

```python
PROMPT = """
You are auditing Kubernetes resource labels for FinOps governance through MCP tools.

Use the available Kubernetes MCP tools to:
1. List all namespaces.
2. For each application namespace (skip kube-* and local-path-storage), fetch deployments, configmaps, and persistent volume claims.
3. Report each resource's name, namespace, kind, and labels exactly as returned by the tools.
4. Flag resources missing owner or cost-center labels.
5. Summarize the label audit in plain English.

Use only data returned by the tools. Do not invent labels or resources.
"""
```

**Highlight:** Multi-step instructions in natural language. The LLM plans multiple `kubectl_get` calls and focuses on label metadata, not a full resource inventory.

> *Talking point: "Same `run_agent` function — we just gave it a FinOps label-audit prompt. MCP returns label metadata in every `kubectl_get` response; the agent reads it so you don't have to grep manually."*

Key lines to call out:

| Line | Why highlight |
|------|---------------|
| `List all namespaces` | First tool call the agent should make |
| `deployments, configmaps, and persistent volume claims` | Resource types where ownership and cost-center labels matter |
| `labels exactly as returned by the tools` | Grounds output in MCP data — no invented labels |
| `Flag resources missing owner or cost-center` | Connects to Section 02a ownership wall and Section 03 tagging problems |
| `Do not invent labels or resources` | Same grounding rule as the query agent |

---

## Block 4 — `main` with higher token limit (lines 20–21)

```python
async def main() -> None:
    print(await run_agent(PROMPT, max_tokens=2048))
```

**Highlight:** `max_tokens=2048` — label audits across namespaces need more room than a namespace list. Passed through to `build_llm` in `mcp_client.py`.

> *Talking point: "The default is 512 tokens from `.env`, but a label audit needs more room for resource names, namespaces, and per-resource label lists."*

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
python3 sections/06-mcp-data-agent/code/label_auditor.py
```

**What it does:** LangChain agent makes multiple MCP tool calls, then prints a plain-English label audit. This may take 30–60 seconds — the LLM is fetching several resource types per namespace.

---

## Expected output

A multi-paragraph or markdown-style summary, for example:

```text
## Kubernetes Label Audit Summary

### Well-tagged resources
- **inventory/inventory-service** (Deployment): owner=inventory-team, cost-center=inventory, app=inventory-service
- **payment/payment-processor** (Deployment): owner=payments-team, cost-center=payment

### Missing owner or cost-center
- **payment/payment-gateway** (Deployment): labels app=payment-gateway, environment=prod — missing owner, cost-center
- **payment/payment-gateway-api** (Deployment): labels app=payment-gateway-api, environment=prod — missing owner, cost-center
- **flight-search/flight-search** (Deployment): labels app=flight-search only — missing owner, cost-center
- **booking-api/booking-api** (Deployment): labels cost-center=booking-engine, app=booking-api — missing owner

### Notes
- kube-system and local-path-storage excluded per instructions
- Labels reported exactly from MCP tool responses
```

**How to read the logs:**

| What you see | Meaning |
|--------------|---------|
| Per-resource label lists | MCP `kubectl_get` responses included label metadata |
| Payment gateway flagged | Matches Section 02a — no owner on payment workloads |
| Inventory namespace looks good | Well-tagged baseline from Section 02 manifests |
| `kube-*` namespaces omitted | LLM respected the skip instruction |
| Truncated output | Increase `max_tokens` or shorten the prompt |
| Missing namespaces | Re-run — LLM tool choice can vary; spot-check with kubectl below |

Spot-check against kubectl:

```bash
kubectl get deploy,configmap,pvc -A --show-labels
```

> *Talking point: "We see label gaps in plain English. Section 07 applies tagging rules and produces structured findings — severity, tickets, and policy scoring."*

---

**Next:** Add policy and structured output → `sections/07-llm-structured-agent`
