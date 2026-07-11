# Guide 0: Understand `query_agent.py`

**Time Budget:** 4–5 mins

**Narrative:** Three files, under 80 lines total — load config, let LangChain pick MCP tools, print a plain-English answer.

**Prerequisites:** Section 05 Supergateway running; `.env` with OpenAI-compatible settings; virtualenv activated.

---

## The flow

```mermaid
sequenceDiagram
    participant Script as query_agent.py
    participant LC as LangChain_ReAct
    participant MCP as Supergateway_MCP
    participant LLM as OpenAI_Compatible_API

    Script->>LC: prompt + MCP tools
    LC->>LLM: which tool and args?
    LLM->>MCP: kubectl_get(...)
    MCP-->>LLM: cluster data
    LLM-->>Script: plain-English answer
    Script->>Script: print answer
```

Open the files:

```bash
cat sections/06-mcp-data-agent/mcp_client.py
cat sections/06-mcp-data-agent/query_agent.py
```

---

### 1) Shared MCP wiring — `mcp_client.py`

```python
load_dotenv(Path(__file__).parents[2] / ".env")
MCP_URL = os.getenv("K8S_MCP_URL", "http://localhost:8000/mcp")
tools, cleanup = await convert_mcp_to_langchain_tools(MCP_SERVERS)
```

**What it does:** Loads the repo-root `.env`, connects to Streamable HTTP at `/mcp`, and converts MCP tools (like `kubectl_get`) into LangChain tools.

> *Talking point: "Both Section 06 scripts share this module — one place for the MCP endpoint."*

---

### 2) The prompt

```python
PROMPT = "list all namespaces"
```

**What it does:** A fixed demo question. Change it to anything — "how many pods in payment?", "show deployments in booking-api".

> *Talking point: "One prompt in. The LLM decides which MCP tool to call and with what arguments."*

---

### 3) LangChain ReAct agent picks the MCP tool

```python
llm = ChatOpenAI(model=..., base_url=..., api_key=...)
agent = create_agent(llm, tools)
result = await agent.ainvoke({"messages": [HumanMessage(content=PROMPT)]})
print(result["messages"][-1].content)
```

**What it does:** LangChain's agent loop handles tool choice — LLM chooses `kubectl_get`, MCP executes it, LLM writes the final answer.

**Why LangChain here?** Without it you'd hand-write: list tools, map schemas, parse tool calls, invoke MCP, call the LLM again. LangChain collapses that into ~10 lines.

> *Talking point: "Same MCP endpoint we proved with curl in Section 05 — now the LLM drives the tool call."*

---

## Compare to `snapshot_collector.py`

| | `query_agent.py` | `snapshot_collector.py` |
|---|---|---|
| **Scope** | One natural-language question | Every namespace, five resource types |
| **Output** | Plain-English answer | Full JSON snapshot with labels |
| **LLM** | Yes — picks MCP tools | No — deterministic loops |
| **Use when** | Teaching prompt → MCP → answer | Collecting everything for downstream analysis |

> *Talking point: "`query_agent.py` asks one question. `snapshot_collector.py` collects everything — see `2_guide.md`."*

---

**Next:** Run the query agent live → `1_guide.md`, then collect the full snapshot → `2_guide.md`
