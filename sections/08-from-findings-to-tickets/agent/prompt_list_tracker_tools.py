"""Standalone demo: ask an LLM to list tracker MCP tools (no mcp_client)."""
import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_mcp_tools import convert_mcp_to_langchain_tools
from langchain_openai import ChatOpenAI

load_dotenv(Path(__file__).parents[3] / ".env")

TRACKER_MCP_URL = os.getenv("TRACKER_MCP_URL", "http://localhost:8086/sse")

TRACKER_MCP_SERVERS = {
    "tracker": {
        "url": TRACKER_MCP_URL,
        "transport": "sse",
    },
}

PROMPT = """
You have issue tracker MCP tools available.

List every tool you can use. For each tool, give its name and a one-line description
of what it does. Do not call any tool. Do not create or update issues.
"""


async def main() -> None:
    tools, cleanup = await convert_mcp_to_langchain_tools(TRACKER_MCP_SERVERS)
    try:
        print(f"Connected to tracker MCP at {TRACKER_MCP_URL} ({len(tools)} tools)\n")
        llm = ChatOpenAI(
            model=os.environ["OPENAI_MODEL_ID"],
            base_url=os.environ["OPENAI_BASE_URL"],
            api_key=os.environ["OPENAI_API_KEY"],
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.2")),
            max_tokens=256,
        )
        agent = create_agent(llm, tools)
        result = await agent.ainvoke({"messages": [HumanMessage(content=PROMPT)]})
        print(result["messages"][-1].content)
    finally:
        await cleanup()


if __name__ == "__main__":
    asyncio.run(main())
