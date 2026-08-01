"""Unified FinOps agent: audit cluster labels via K8s MCP and post tickets via tracker MCP."""
import asyncio
from pathlib import Path

from mcp_client import run_agent

# Keep the tool surface small so the agent spends steps on create_issue, not discovery.
ALLOWED_TOOLS = {"kubectl_get", "create_issue", "list_issues"}

PROMPT = """
You are a FinOps agent with Kubernetes kubectl_get and issue tracker tools (create_issue, list_issues).

Execute this exact plan — do not invent extra discovery steps:

Step 1 — Collect (1 kubectl_get call only):
- kubectl_get resourceType=deployments namespace=payment output=json

Step 2 — Evaluate labels on each Deployment against the tagging rules.
A required tag is missing when NONE of its label_mappings keys appear on the resource.

Step 3 — For EVERY non-compliant Deployment, call create_issue (one call per resource).
Required fields:
- title: "[FinOps] {namespace}/{resource_name} - {CATEGORY}"
- summary, body, namespace, resource_name, resource_kind
- category: missing-owner | unallocated | orphaned | missing-labels
- priority: critical | high | medium | low
- suggested_owner, suggested_cost_center, reasoning
- source: "mcp-llm-agent"

Step 4 — Call list_issues once and stop.

Hard rules:
- Follow Step 1's scope exactly — do not invent extra kubectl_get calls.
- Do not fetch configmaps, PVCs, or individual resources by name.
- Do not write a plain-English audit report instead of creating tickets.
- Your run is a failure if you end without at least one create_issue call when
  non-compliant Deployments exist in the scoped result set.
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
        allowed_tools=ALLOWED_TOOLS,
    )
    print(result)
    print("\n--- Done. Verify tickets at http://localhost:8085 ---")


if __name__ == "__main__":
    asyncio.run(main())
