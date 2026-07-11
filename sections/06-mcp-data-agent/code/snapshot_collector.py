"""Ask a LangChain agent to inspect the cluster and print its final answer."""
import asyncio

from mcp_client import run_agent

PROMPT = """
You are collecting a Kubernetes FinOps inventory through MCP tools.

Use the available Kubernetes MCP tools to:
1. List all namespaces.
2. Fetch deployments, pods, services, persistent volume claims, and configmaps across all namespaces.
3. Ignore kube-* namespaces and local-path-storage when summarizing application resources.
4. Summarize the inventory in plain English.

Include resource names, namespaces, kinds, and labels when labels are present.
Use only data returned by the tools. Do not invent resources.
"""


async def main() -> None:
    print(await run_agent(PROMPT, max_tokens=2048))


if __name__ == "__main__":
    asyncio.run(main())
