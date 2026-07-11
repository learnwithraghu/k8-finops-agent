"""Shared MCP connection helpers for Section 06 scripts."""
import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain_core.tools import BaseTool
from langchain_mcp_tools import convert_mcp_to_langchain_tools

load_dotenv(Path(__file__).parents[2] / ".env")

MCP_URL = os.getenv("K8S_MCP_URL", "http://localhost:8000/mcp")
MCP_SERVERS = {
    "k8s": {
        "url": MCP_URL,
        "transport": "streamable_http",
    }
}


async def get_mcp_tools():
    return await convert_mcp_to_langchain_tools(MCP_SERVERS)


def tool_by_name(tools: list[BaseTool], name: str) -> BaseTool:
    tool = next((t for t in tools if t.name == name), None)
    if tool is None:
        raise RuntimeError(f"MCP tool not found: {name}")
    return tool


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
