"""Standalone: connect to tracker MCP and list available tools (no mcp_client)."""
import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_mcp_tools import convert_mcp_to_langchain_tools

load_dotenv(Path(__file__).parents[3] / ".env")

TRACKER_MCP_URL = os.getenv("TRACKER_MCP_URL", "http://localhost:8086/sse")

TRACKER_MCP_SERVERS = {
    "tracker": {
        "url": TRACKER_MCP_URL,
        "transport": "sse",
    },
}


async def main() -> None:
    tools, cleanup = await convert_mcp_to_langchain_tools(TRACKER_MCP_SERVERS)
    try:
        print(f"Tracker MCP OK — {len(tools)} tools via {TRACKER_MCP_URL}")
        for tool in tools:
            description = (tool.description or "").strip()
            if description:
                print(f"  - {tool.name}: {description}")
            else:
                print(f"  - {tool.name}")
    finally:
        await cleanup()


if __name__ == "__main__":
    asyncio.run(main())
