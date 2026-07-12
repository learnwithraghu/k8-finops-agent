"""Ask a LangChain agent to audit labels against tagging rules and print its final answer."""
import asyncio
from pathlib import Path

from mcp_client import run_agent

TAGGING_RULES_PATH = Path(__file__).parents[1] / "config" / "tagging-rules.yaml"

PROMPT = """
You are auditing Kubernetes resource labels for FinOps governance through MCP tools.

Use the available Kubernetes MCP tools to:
1. List all namespaces.
2. For each application namespace (skip kube-* and excluded namespaces from the rules),
   fetch deployments, configmaps, and persistent volume claims.
3. Report each resource's name, namespace, kind, and labels exactly as returned by the tools.
4. Evaluate each resource against the tagging rules provided separately.
5. Flag resources that violate required tags or label mappings.
6. Summarize the label audit in plain English, grouped by namespace.

Use only data returned by the tools. Do not invent labels or resources.
"""


def load_tagging_rules() -> str:
    if not TAGGING_RULES_PATH.exists():
        raise FileNotFoundError(f"Tagging rules not found: {TAGGING_RULES_PATH}")
    return TAGGING_RULES_PATH.read_text()


async def main() -> None:
    print(
        await run_agent(
            PROMPT,
            tagging_rules=load_tagging_rules(),
            max_tokens=2048,
        )
    )


if __name__ == "__main__":
    asyncio.run(main())
