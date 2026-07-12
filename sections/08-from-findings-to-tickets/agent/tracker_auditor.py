"""Run the Section 06 label audit via MCP, structure findings, and post to the tracker."""
import asyncio
import logging
from pathlib import Path

from mcp_client import run_agent
from structure import structure_findings
from tracker_client import post_tickets

logging.basicConfig(level=logging.INFO)

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

TAGGING_RULES_PATH = (
    Path(__file__).parents[2] / "07-llm-structured-agent" / "config" / "tagging-rules.yaml"
)


def load_tagging_rules() -> str:
    if TAGGING_RULES_PATH.exists():
        return TAGGING_RULES_PATH.read_text()
    return ""


async def main() -> None:
    audit_text = await run_agent(PROMPT, max_tokens=2048)
    batch = structure_findings(audit_text, load_tagging_rules())
    await post_tickets(batch)
    print(f"\n--- Posted {len(batch.tickets)} ticket(s) to the issue tracker ---")


if __name__ == "__main__":
    asyncio.run(main())
