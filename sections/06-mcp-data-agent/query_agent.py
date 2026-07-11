"""Prompt → LangChain agent → MCP tools → plain-text answer."""
import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from mcp_client import get_mcp_tools

PROMPT = "list all namespaces"


async def main() -> None:
    tools, cleanup = await get_mcp_tools()
    try:
        llm = ChatOpenAI(
            model=os.environ["OPENAI_MODEL_ID"],
            base_url=os.environ["OPENAI_BASE_URL"],
            api_key=os.environ["OPENAI_API_KEY"],
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.3")),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "256")),
        )
        agent = create_agent(llm, tools)
        result = await agent.ainvoke({"messages": [HumanMessage(content=PROMPT)]})
        print(result["messages"][-1].content)
    finally:
        await cleanup()


if __name__ == "__main__":
    asyncio.run(main())
