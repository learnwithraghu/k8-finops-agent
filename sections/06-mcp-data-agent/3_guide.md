# Video 3: LangChain Agent Shared Wiring

**Time Budget:** 4–5 mins

**Narrative:** Every Section 06 script shares one module for MCP connection, LLM setup, and the LangChain agent loop. Walk through `mcp_client.py` block by block before running any agent script.

**Prerequisites:** [`2_guide.md`](2_guide.md) — MCP container running; `validate_mcp.py` passed.

---

Open the file:

```bash
cat sections/06-mcp-data-agent/code/mcp_client.py
```

---

### Block 1 — Module docstring (lines 1–5)

```python
"""Shared LangChain + MCP helpers for Section 06 scripts.

Expects the persistent HTTP MCP container from Guide 2 (native Streamable HTTP on
http://localhost:8000/mcp). No Supergateway required.
"""
```

**Highlight:** The contract — standalone HTTP MCP, not Supergateway.

> *Talking point: "Think of this file as the bridge between our scripts and the cluster — the agents never talk to kubectl directly."*

---

### Block 2 — Imports (lines 6–16)

```python
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain_mcp_tools import convert_mcp_to_langchain_tools
```

**Highlight:** `convert_mcp_to_langchain_tools` — turns MCP tools into LangChain tools the agent can call.

> *Talking point: "We don't hand-write tool schemas — the converter picks them up automatically from the MCP handshake."*

---

### Block 3 — Load `.env` and MCP config (lines 18–26)

```python
load_dotenv(Path(__file__).parents[3] / ".env")

MCP_URL = os.getenv("K8S_MCP_URL", "http://localhost:8000/mcp")
MCP_SERVERS = {
    "k8s": {
        "url": MCP_URL,
        "transport": "streamable_http",
    }
}
```

**Highlight:** `parents[3]` reaches the repo root from `code/`. `streamable_http` matches the standalone container from Guide 2.

> *Talking point: "Same `.env` as the rest of the course — you'd only override `K8S_MCP_URL` if the endpoint moves somewhere else."*

---

### Block 4 — `decode_tool_result` (lines 29–38)

```python
def decode_tool_result(result: Any) -> dict:
    ...
```

**Highlight:** MCP tool output may arrive as a dict or a JSON string. This normalizes it so callers can always use `.get("items", [])`.

> *Talking point: "The validation scripts use this helper. Agents usually get structured data through LangChain, but when you call a tool directly you need to parse the result yourself."*

---

### Block 5 — `tool_by_name` (lines 41–45)

```python
def tool_by_name(tools: list[BaseTool], name: str) -> BaseTool:
    ...
```

**Highlight:** Looks up a tool by name — `validate_mcp.py` uses this to grab `kubectl_get` without going through the LLM.

> *Talking point: "Need deterministic behavior? Call a tool by name. Want flexibility? Let the agent figure it out."*

---

### Block 6 — `get_mcp_tools` (lines 48–49)

```python
async def get_mcp_tools():
    return await convert_mcp_to_langchain_tools(MCP_SERVERS)
```

**Highlight:** Opens the MCP session and returns `(tools, cleanup)`. Always call `cleanup` in a `finally` block.

> *Talking point: "This is where we actually connect — HTTP handshake, discover the tools, wrap them for LangChain."*

---

### Block 7 — `build_llm` (lines 52–59)

```python
def build_llm(max_tokens: int | None = None) -> ChatOpenAI:
    return ChatOpenAI(
        model=os.environ["OPENAI_MODEL_ID"],
        base_url=os.environ["OPENAI_BASE_URL"],
        api_key=os.environ["OPENAI_API_KEY"],
        ...
    )
```

**Highlight:** Reads OpenAI-compatible settings from `.env`. `max_tokens` can be overridden for longer label audit reports.

> *Talking point: "MCP handles reading the cluster; the LLM picks which tools to call and writes the answer. Two separate pieces working together."*

---

### Block 8 — `run_agent` (lines 62–69)

```python
async def run_agent(prompt: str, max_tokens: int | None = None) -> str:
    tools, cleanup = await get_mcp_tools()
    try:
        agent = create_agent(build_llm(max_tokens=max_tokens), tools)
        result = await agent.ainvoke({"messages": [HumanMessage(content=prompt)]})
        return result["messages"][-1].content
    finally:
        await cleanup()
```

**Highlight:** The full agent loop in one function — connect, run ReAct agent, return the final LLM message, always cleanup.

> *Talking point: "Both `query_agent.py` and `label_auditor.py` are just thin wrappers around this — change the prompt, not the plumbing."*

---

**Next:** Run your first agent → `4_guide.md`
