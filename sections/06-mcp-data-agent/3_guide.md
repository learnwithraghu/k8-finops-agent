# Video 3: LangChain Agent Shared Wiring

**Time Budget:** 4–5 mins

**Prerequisites:** [`2_guide.md`](2_guide.md) — MCP container running; `validate_mcp.py` passed.

> **Legend:** Blockquote lines are on-screen actions — do not read them aloud. Everything else is your script.

---

### Opening (~20 sec)

In Video 2 we started the MCP server and validated it with Python. Before we run any agent, let's walk through the one file every Section 06 script shares — `mcp_client.py`. This is the bridge between our prompts and the cluster. The agents never talk to kubectl directly.

> **Do:** Open `sections/06-mcp-data-agent/code/mcp_client.py` in the editor.

---

### Block 1 — Module docstring (lines 1–5)

```python
"""Shared LangChain + MCP helpers for Section 06 scripts.

Expects the persistent HTTP MCP container from Guide 2 (native Streamable HTTP on
http://localhost:8000/mcp). No Supergateway required.
"""
```

This docstring is the contract for the whole section. We expect the standalone HTTP MCP container from Guide 2 — native Streamable HTTP, no Supergateway in the middle. Every script in this folder imports from here.

---

### Block 2 — Imports (lines 6–16)

```python
import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain_mcp_tools import convert_mcp_to_langchain_tools
```

These imports split into three jobs. Standard library for paths and JSON. LangChain for the agent loop and the OpenAI-compatible LLM. And `langchain-mcp-tools` — that's the piece that converts MCP tools into LangChain tools the agent can call. We don't hand-write tool schemas. The converter discovers them from the MCP handshake automatically.

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

First we load the repo-root `.env` — `parents[3]` walks up from `code/` to the project root. Same API keys and model settings as the rest of the course.

Then we define where MCP lives. `MCP_URL` defaults to the container we started in Guide 2. You'd only override `K8S_MCP_URL` if the endpoint moves. The transport is `streamable_http` — that matches the standalone container, not the Supergateway setup from Section 05.

---

### Block 4 — `decode_tool_result` (lines 29–38)

```python
def decode_tool_result(result: Any) -> dict:
    if isinstance(result, dict):
        return result
    text = str(result).strip()
    if not text:
        return {"items": []}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"items": []}
```

MCP tool output can arrive as a dict or as a JSON string depending on how it was called. This helper normalizes either shape so callers can always do `.get("items", [])`.

`validate_mcp.py` uses this when it calls `kubectl_get` directly. The LangChain agent usually gets structured data through the framework — but when you call a tool yourself, you parse the result here.

---

### Block 5 — `tool_by_name` (lines 41–45)

```python
def tool_by_name(tools: list[BaseTool], name: str) -> BaseTool:
    tool = next((t for t in tools if t.name == name), None)
    if tool is None:
        raise RuntimeError(f"MCP tool not found: {name}")
    return tool
```

Simple lookup — find a tool by name in the list MCP returned. `validate_mcp.py` uses this to grab `kubectl_get` without going through the LLM.

Two patterns in this section: need deterministic behavior, call a tool by name. Want flexibility, let the agent choose. Same connection, different caller.

---

### Block 6 — `get_mcp_tools` (lines 48–49)

```python
async def get_mcp_tools():
    return await convert_mcp_to_langchain_tools(MCP_SERVERS)
```

This is where we actually connect. HTTP handshake, discover the tools, wrap them for LangChain. It returns a tuple — the tools list and a cleanup callback. Always call cleanup in a `finally` block so the session closes cleanly.

---

### Block 7 — `build_llm` (lines 52–59)

```python
def build_llm(max_tokens: int | None = None) -> ChatOpenAI:
    return ChatOpenAI(
        model=os.environ["OPENAI_MODEL_ID"],
        base_url=os.environ["OPENAI_BASE_URL"],
        api_key=os.environ["OPENAI_API_KEY"],
        temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.3")),
        max_tokens=max_tokens or int(os.getenv("OPENAI_MAX_TOKENS", "512")),
    )
```

This builds the LLM from `.env` — model, base URL, API key. Temperature and max tokens have sensible defaults, but callers can override `max_tokens` for longer answers. The label auditor in Video 5 passes a higher limit because label reports run longer than a one-line namespace list.

MCP reads the cluster. The LLM decides which tools to call and writes the answer. Two separate pieces, one shared module.

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

This is the full agent loop in one function. Connect to MCP, create the LangChain agent with the LLM and tools, invoke it with your prompt, return the final message, and always clean up.

Both `query_agent.py` and `label_auditor.py` are thin wrappers around this — you change the prompt, not the plumbing. That's the pattern for the rest of the section.

---

### Close (~10 sec)

That's the shared wiring. Next we run the smallest possible agent — one prompt, one call to `run_agent`. Open `4_guide.md`.

> **Do:** Save the file. Keep the MCP container running.
