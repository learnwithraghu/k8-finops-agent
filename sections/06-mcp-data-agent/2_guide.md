# Demo 2: Run `code/query_agent.py` and Observe the Answer

**Time Budget:** 3–4 mins

**Narrative:** One prompt — "list all namespaces". The LangChain agent picks MCP tools, reads the cluster, and returns the LLM's final answer.

**Prerequisites:** [`1_guide.md`](1_guide.md) — understand the code first; MCP container running; virtualenv activated.

---

### 1) Confirm MCP is still reachable

```bash
source .venv/bin/activate
python3 sections/06-mcp-data-agent/code/validate_mcp.py
```

**What it does:** Quick Python check that the persistent MCP container is still up. If this fails, restart the container from `0_guide.md`.

---

### 2) Confirm LLM configuration

```bash
grep OPENAI .env
```

**What it does:** Shows the OpenAI-compatible endpoint settings. `code/mcp_client.py` loads these from the repo-root `.env`.

> *Talking point: "The LLM endpoint is separate from MCP. MCP reads the cluster; the LLM chooses tools and writes the answer."*

---

### 3) Run the script

```bash
python3 sections/06-mcp-data-agent/code/query_agent.py
```

**What it does:** LangChain ReAct agent picks `kubectl_get` through MCP, then prints a short plain-English summary.

> *Expected: A few sentences listing airline namespaces like `booking-api`, `flight-search`, `inventory`, `payment`.*

> *Talking point: "The LLM chose the tool — we didn't hardcode `kubectl_get`. Change `PROMPT` in `code/query_agent.py` to ask anything about the cluster."*

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

> *Talking point: "This answer is useful but small — one question at a time. The next demo uses the same agent wiring with a broader inventory prompt."*

---

**Next:** Run the inventory agent → `3_guide.md`
