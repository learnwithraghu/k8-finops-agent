"""Unified FinOps agent: audit cluster labels via K8s MCP and post tickets via tracker MCP."""
import asyncio
from pathlib import Path

from mcp_client import run_agent

PROMPT = """
You are a FinOps agent with access to Kubernetes MCP tools and issue tracker MCP tools.

Your job:
1. Use Kubernetes MCP tools to list namespaces and fetch deployments, configmaps, and
   persistent volume claims for each application namespace (skip kube-* and local-path-storage).
2. Evaluate each resource against the tagging rules provided in the system message.
3. For every non-compliant resource, call the tracker create_issue tool with a complete payload.
   Do not create tickets for compliant resources.
4. When finished, call list_issues to confirm tickets were created.

create_issue fields (use all that apply):
- title: "[FinOps] {namespace}/{resource_name} - {CATEGORY}"
- summary: one-line description of the finding
- body: details including labels found
- namespace, resource_name, resource_kind
- category: e.g. missing-owner, unallocated, orphaned
- priority: critical | high | medium | low
- suggested_owner, suggested_cost_center, reasoning
- source: "mcp-llm-agent"

Rules:
- Use only data returned by Kubernetes MCP tools. Do not invent resources or labels.
- Do not finish with a plain-English audit report. Your job is done when tickets are created.
- Create one ticket per distinct finding.
"""

TAGGING_RULES_PATH = (
    Path(__file__).parents[2] / "07-llm-structured-agent" / "config" / "tagging-rules.yaml"
)


def load_tagging_rules() -> str:
    if TAGGING_RULES_PATH.exists():
        return TAGGING_RULES_PATH.read_text()
    return ""


async def main() -> None:
    result = await run_agent(
        PROMPT,
        tagging_rules=load_tagging_rules(),
        max_tokens=4096,
    )
    print(result)
    print("\n--- Done. Verify tickets at http://localhost:8085 ---")


if __name__ == "__main__":
    asyncio.run(main())
