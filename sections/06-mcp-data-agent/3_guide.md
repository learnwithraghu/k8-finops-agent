# Demo 3: Run the Inventory Agent

**Time Budget:** 3 mins

**Narrative:** The query agent answers one small question. The inventory agent uses the same LangChain + MCP path with a larger prompt: inspect namespaces and common Kubernetes resources, then print the LLM's final summary.

**Prerequisites:** [`2_guide.md`](2_guide.md) — query agent working; MCP container running; virtualenv activated.

---

### 1) Confirm MCP is still reachable

```bash
source .venv/bin/activate
python3 sections/06-mcp-data-agent/code/validate_mcp.py
```

**What it does:** Quick Python check before running the inventory agent. If this fails, restart the MCP container from `0_guide.md`.

---

### 2) Peek at the inventory agent code

```bash
cat sections/06-mcp-data-agent/code/snapshot_collector.py
```

**What it does:** Shows the broader inventory prompt. The script imports the shared agent runner from `code/mcp_client.py`, asks the LLM to use MCP tools, and prints the final LLM response.

> *Talking point: "Same MCP tools, same LangChain agent path. Only the prompt changed."*

---

### 3) Run the inventory agent

```bash
python3 sections/06-mcp-data-agent/code/snapshot_collector.py
```

**What it does:** Connects to MCP through `code/mcp_client.py`, lets LangChain choose `kubectl_get` calls, and prints the final summary from the LLM.

> *Talking point: "This is still agent-driven. The LLM chooses tool calls, MCP returns real cluster data, and the LLM writes the final answer."*

---

### 4) Review the output

```bash
kubectl get deploy,pod,svc,pvc,configmap -A
```

**What it does:** Gives you a quick kubectl spot-check against the LLM's inventory summary.

> *Expected: A plain-English or markdown-style summary listing namespaces and application resources. Labels should appear when the MCP response includes them.*

> *Talking point: "For now we are printing the LLM's final output. Section 07 is where we add structured output and policy scoring."*

---

**Next:** Add policy and structured output → `sections/07-llm-structured-agent`
