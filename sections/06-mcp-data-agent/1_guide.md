# Demo 1: Run `query_agent.py` and Observe the Answer

**Time Budget:** 3–4 mins

**Narrative:** One prompt — "list all namespaces". The LangChain agent picks MCP tools, reads the cluster, and returns a plain-English summary.

**Prerequisites:** [`0_guide.md`](0_guide.md) — understand the code first; virtualenv activated.

---

### 1) Confirm MCP endpoint is alive

```bash
curl -s http://localhost:8000/healthz
```

**What it does:** Quick health check before running the agent. If this fails, Supergateway is not running.

> *Expected: `ok`*

---

### 2) Confirm LLM configuration

```bash
grep OPENAI .env
```

**What it does:** Shows the OpenAI-compatible endpoint settings. The script reads these at startup via `mcp_client.py` and `query_agent.py`.

> *Talking point: "The LLM endpoint is separate from MCP. MCP reads the cluster; the LLM chooses tools and writes the answer."*

---

### 3) Run the script

```bash
source .venv/bin/activate
python3 sections/06-mcp-data-agent/query_agent.py
```

**What it does:** LangChain ReAct agent picks `kubectl_get` through MCP, then prints a short plain-English summary.

> *Expected: A few sentences listing airline namespaces like `booking-api`, `flight-search`, `inventory`, `payment`.*

> *Talking point: "The LLM chose the tool — we didn't hardcode `kubectl_get`. Change `PROMPT` to ask anything about the cluster."*

---

### 4) Spot-check against kubectl

```bash
kubectl get ns
```

**What it does:** Confirms the LLM's answer matches what kubectl shows.

> *Talking point: "The LLM summarized real cluster data — MCP is the source of truth."*

---

### 5) What we learned

- **Prompt in** → `list all namespaces`
- **LLM** → picks MCP tool + arguments
- **MCP out** → raw cluster data
- **LLM** → plain-English answer

> *Talking point: "This answer is useful but unstructured — one question at a time. FinOps needs a full snapshot with labels — that's `snapshot_collector.py` in Demo 2."*

---

**Next:** Collect a structured cluster snapshot → `2_guide.md`
