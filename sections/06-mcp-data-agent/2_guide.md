# Demo 2: Run `simple_mcp_llm.py` and Observe the Answer

**Time Budget:** 3–4 mins

**Narrative:** One prompt — "list all namespaces". MCP reads the cluster, the LLM returns a plain-English summary.

**Prerequisites:** [`0_guide.md`](0_guide.md) — understand the code first.

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

**What it does:** Shows the OpenAI-compatible endpoint settings. The script reads these at startup.

> *Talking point: "The LLM endpoint is separate from MCP. MCP reads the cluster; the LLM reads the MCP result and writes the answer."*

---

### 3) Run the script

```bash
python3 sections/06-mcp-data-agent/simple_mcp_llm.py
```

**What it does:** Calls `kubectl_get` for all namespaces through MCP, then prints a short LLM summary.

> *Expected: A few sentences listing airline namespaces like `booking-api`, `flight-search`, `inventory`, `payment`.*

> *Talking point: "Same `kubectl_get` tool we proved with curl in Section 05 — now driven from Python."*

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
- **MCP out** → raw namespace JSON
- **LLM** → plain-English answer

> *Talking point: "This answer is useful but unstructured — no severity, no tickets, no policy. Section 07 adds tagging rules and structured findings."*

---

**Optional:** For a full cluster snapshot without the LLM, see `1_guide.md` (`agent.py`).

**Next:** Add policy and structured output → `sections/07-llm-structured-agent`
