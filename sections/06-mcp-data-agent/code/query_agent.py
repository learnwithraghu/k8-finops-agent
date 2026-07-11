"""Prompt -> LangChain agent -> MCP tools -> plain-text answer."""
import asyncio

from mcp_client import run_agent

PROMPT = "list all namespaces"


async def main() -> None:
    print(await run_agent(PROMPT))


if __name__ == "__main__":
    asyncio.run(main())
