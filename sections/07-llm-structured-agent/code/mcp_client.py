"""Shared LangChain + MCP helpers for Section 07 scripts.

Expects the persistent HTTP MCP container from Section 06 (native Streamable HTTP on
http://localhost:8000/mcp). No Supergateway required.
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
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


async def run_agent(
    prompt: str,
    max_tokens: int | None = None,
    tagging_rules: str | None = None,
) -> str:
    tools, cleanup = await get_mcp_tools()
    try:
        agent = create_agent(build_llm(max_tokens=max_tokens), tools)
        messages = []
        if tagging_rules:
            messages.append(
                SystemMessage(
                    content=(
                        "Apply the tagging rules below when evaluating cluster resources. "
                        "Treat label_mappings as the only accepted keys for each required tag. "
                        "Do not invent extra policy, exclusions, or judgments beyond this YAML.\n\n"
                        f"Tagging rules (YAML):\n{tagging_rules}"
                    )
                )
            )
        messages.append(HumanMessage(content=prompt))
        result = await agent.ainvoke({"messages": messages})
        return result["messages"][-1].content
    finally:
        await cleanup()
