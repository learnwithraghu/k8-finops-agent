"""Connect to tracker MCP and list available tools."""
import asyncio

from mcp_client import TRACKER_MCP_URL, get_tracker_mcp_tools


async def main() -> None:
    tools, cleanup = await get_tracker_mcp_tools()
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
