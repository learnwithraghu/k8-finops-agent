"""Ask a LangChain agent to audit labels against tagging rules and print its final answer."""
import asyncio
from pathlib import Path

from mcp_client import run_agent

TAGGING_RULES_PATH = Path(__file__).parents[1] / "config" / "tagging-rules.yaml"

PROMPT = """
You are auditing Kubernetes resource labels for FinOps governance through MCP tools.

Use the available Kubernetes MCP tools to:
1. List all namespaces.
2. For each application namespace (skip only namespaces listed in excluded_namespaces;
   also skip kube-* namespaces), fetch deployments, configmaps, and persistent volume claims.
3. Report each resource's name, namespace, kind, and labels exactly as returned by the tools.
4. Evaluate each resource against the tagging rules provided separately.
5. Flag resources that violate required tags or label mappings.
6. Summarize the full label audit in plain English, grouped by namespace. Cover every
   audited namespace and resource — do not truncate mid-report.

Evaluation rules (follow strictly; do not invent policy):
- A required tag is present if ANY key listed under that tag in label_mappings appears
  on the resource (for example, `app` satisfies `application`).
- Do not call a mapped key non-standard, legacy, or invalid when it is in label_mappings.
- Use only required_tags, label_mappings, cost_centers, environments, tiers,
  compliance_levels, resource_types, and excluded_namespaces from the rules.
- Do not invent exclusions, bonus labels, recommended tags, or extra commentary
  beyond what the rules define.

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
