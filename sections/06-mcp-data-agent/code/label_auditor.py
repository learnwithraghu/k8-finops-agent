"""Ask a LangChain agent to audit cluster labels via MCP and print its final answer."""
import asyncio

from mcp_client import run_agent

PROMPT = """
You are auditing Kubernetes resource labels for FinOps governance through MCP tools.

Use the available Kubernetes MCP tools to:
1. List all namespaces.
2. For each application namespace (skip kube-* and local-path-storage), fetch deployments, configmaps, and persistent volume claims.
3. Report each resource's name, namespace, kind, and labels exactly as returned by the tools.
4. Flag resources missing owner or cost-center labels.
5. Summarize the label audit in plain English.

Use only data returned by the tools. Do not invent labels or resources.
"""


async def main() -> None:
    print(await run_agent(PROMPT, max_tokens=2048))


if __name__ == "__main__":
    asyncio.run(main())
