"""Prompt → MCP → output. Minimal teaching script."""
import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from openai import OpenAI

load_dotenv(Path(__file__).parents[2] / ".env")

PROMPT = "list all namespaces"
MCP_URL = "http://localhost:8000/mcp"


def tool_text(result):
    return "".join(p.text for p in result.content if getattr(p, "type", None) == "text")


async def main():
    # MCP Python SDK talks to Supergateway over Streamable HTTP (Section 05).
    # async with opens the connection, runs the MCP handshake, and closes it when done.
    async with streamablehttp_client(MCP_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "kubectl_get",
                {"resourceType": "namespaces", "allNamespaces": True, "output": "name"},
            )
            data = tool_text(result)

    client = OpenAI(
        base_url=os.environ["OPENAI_BASE_URL"],
        api_key=os.environ["OPENAI_API_KEY"],
    )
    answer = client.chat.completions.create(
        model=os.environ["OPENAI_MODEL_ID"],
        messages=[
            {
                "role": "user",
                "content": f"{PROMPT}\n\nCluster data:\n{data}\n\nAnswer in 2-3 sentences.",
            }
        ],
        max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "1024")),
        temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.3")),
    )
    print(answer.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(main())
