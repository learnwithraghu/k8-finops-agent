"""Agent: prompt → LLM picks MCP tool → answer."""
import asyncio
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from openai import OpenAI

load_dotenv(Path(__file__).parents[2] / ".env")

PROMPT = "list all namespaces"
MCP_URL = "http://localhost:8000/mcp"
KUBECTL_GET = {
    "type": "function",
    "function": {
        "name": "kubectl_get",
        "description": "Get Kubernetes resources (namespaces, pods, deployments, etc.)",
        "parameters": {
            "type": "object",
            "properties": {
                "resourceType": {"type": "string"},
                "allNamespaces": {"type": "boolean"},
                "output": {"type": "string"},
            },
            "required": ["resourceType"],
        },
    },
}


def tool_text(result):
    return "".join(p.text for p in result.content if getattr(p, "type", None) == "text")


async def main():
    client = OpenAI(
        base_url=os.environ["OPENAI_BASE_URL"],
        api_key=os.environ["OPENAI_API_KEY"],
    )
    model = os.environ["OPENAI_MODEL_ID"]
    opts = {
        "max_tokens": int(os.getenv("OPENAI_MAX_TOKENS", "1024")),
        "temperature": float(os.getenv("OPENAI_TEMPERATURE", "0.3")),
    }

    async with streamablehttp_client(MCP_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 1) LLM picks which MCP tool to call
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": PROMPT}],
                tools=[KUBECTL_GET],
                **opts,
            )
            call = response.choices[0].message.tool_calls[0]

            # 2) Run the tool MCP chose
            result = await session.call_tool(
                call.function.name, json.loads(call.function.arguments)
            )

            # 3) LLM answers using the tool result
            final = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": PROMPT},
                    response.choices[0].message,
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": tool_text(result),
                    },
                ],
                **opts,
            )
            print(final.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(main())
