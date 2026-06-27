"""MCP tracker tools — auto-discovered via langchain-mcp-tools.

No manual session management, no argument mapping.
The LLM calls create_issue directly when it finds violations.
"""

from langchain_mcp_tools import McpServerUrlBasedConfig, convert_mcp_to_langchain_tools


async def load_tracker_tools(mcp_url: str = "http://localhost:8086/mcp"):
    """Connect to tracker MCP, return tools as {name: BaseTool}."""
    tools, cleanup = await convert_mcp_to_langchain_tools(
        {
            "issue-tracker": McpServerUrlBasedConfig(
                url=mcp_url,
                transport="sse",
                timeout=30.0,
            ),
        }
    )
    return {t.name: t for t in tools}
