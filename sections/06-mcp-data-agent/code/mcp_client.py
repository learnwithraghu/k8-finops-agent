"""Shared LangChain + MCP helpers for Section 06 scripts.

Expects the persistent HTTP MCP container from Guide 2 (native Streamable HTTP on
http://localhost:8000/mcp). No Supergateway required.
"""
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

load_dotenv(Path(__file__).parents[3] / ".env")

MCP_URL = os.getenv("K8S_MCP_URL", "http://localhost:8000/mcp")
MCP_SERVERS = {
    "k8s": {
        "url": MCP_URL,
        "transport": "streamable_http",
    }
}


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


def tool_by_name(tools: list[BaseTool], name: str) -> BaseTool:
    tool = next((t for t in tools if t.name == name), None)
    if tool is None:
        raise RuntimeError(f"MCP tool not found: {name}")
    return tool


async def get_mcp_tools():
    return await convert_mcp_to_langchain_tools(MCP_SERVERS)


def build_llm(max_tokens: int | None = None) -> ChatOpenAI:
    return ChatOpenAI(
        model=os.environ["OPENAI_MODEL_ID"],
        base_url=os.environ["OPENAI_BASE_URL"],
        api_key=os.environ["OPENAI_API_KEY"],
        temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.3")),
        max_tokens=max_tokens or int(os.getenv("OPENAI_MAX_TOKENS", "512")),
    )


async def run_agent(prompt: str, max_tokens: int | None = None) -> str:
    tools, cleanup = await get_mcp_tools()
    try:
        agent = create_agent(build_llm(max_tokens=max_tokens), tools)
        result = await agent.ainvoke({"messages": [HumanMessage(content=prompt)]})
        return result["messages"][-1].content
    finally:
        await cleanup()
