"""LLM-powered FinOps analysis using LangChain + an OpenAI-compatible endpoint.

For each resource, a single prompt sends the scanned K8s metadata plus the
FinOps tagging policy to the LLM. The LLM returns one structured decision that
covers both the compliance verdict and (if needed) a GitHub issue draft.
"""

import json
import logging
import os
from typing import Dict, Any, List, Tuple

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from agent.scanner import K8sResource

logger = logging.getLogger(__name__)


class ResourceDecision(BaseModel):
    """Structured LLM output: compliance verdict + issue draft for one resource."""
    is_compliant: bool = Field(description="True if all required tags are present and the resource is not an orphaned PVC")
    category: str = Field(description="One of: tagged, unallocated, unowned, orphaned, unknown, other")
    missing_tags: List[str] = Field(description="Required tags that are missing or empty")
    reason: str = Field(description="Short human-readable reason for the compliance decision")
    should_create_issue: bool = Field(description="Whether to create a GitHub issue for this resource")
    issue_title: str = Field(description="GitHub issue title in format: [FinOps] namespace/name - CATEGORY")
    issue_body: str = Field(description="Markdown body with summary, missing tags, and remediation steps")
    issue_labels: List[str] = Field(description="GitHub issue labels")
    priority: str = Field(description="Priority level: critical, high, medium, or low")
    suggested_cost_center: str = Field(description="Suggested cost center for the resource")
    suggested_owner: str = Field(description="Suggested team owner for the resource")
    suggested_tags: Dict[str, str] = Field(description="Suggested tags to apply")


PROMPT_TEMPLATE = """You are a FinOps agent for a Kubernetes-based airline platform.

Decide whether the following resource complies with the FinOps tagging policy below,
and draft a GitHub issue for the owning team if it does not.

Resource Facts:
- Name: {resource_name}
- Namespace: {namespace}
- Kind: {kind}
- Labels: {labels}
- Annotations: {annotations}
- CPU Request: {cpu_request}m
- Memory Request: {memory_request}Mi
- Replicas: {replicas}
- PVCs: {pvc_names}
- PVC Size (GB): {pvc_size_gb}
- Orphaned PVC: {is_orphaned}

FinOps Tagging Policy:
{tagging_rules}

{format_instructions}

Rules:
- Compare the resource's labels against `required_tags`, using `label_mappings` to
  recognize aliases (e.g. `app.kubernetes.io/owner` counts as `owner`).
- A resource where "Orphaned PVC: true" is never compliant - set category="orphaned"
  and should_create_issue=true regardless of its labels.
- If a resource has no `cost-center` tag (or alias), category="unallocated".
- If a resource has a cost-center but no `owner`, category="unowned".
- If the resource is in the "default" namespace with no labels at all, category="unknown".
- If all required tags are present and the PVC (if any) is mounted, set
  is_compliant=true, category="tagged", missing_tags=[], should_create_issue=false.
- Keep issue titles concise: "[FinOps] namespace/name - CATEGORY".
- Body should include: summary, missing tags, and remediation steps.
- Prefer concrete team names for suggested_owner.
"""


def analyze_resource(
    resource: K8sResource,
    model_id: str,
    base_url: str = None,
    api_key: str = None,
    max_tokens: int = 1024,
    temperature: float = 0.3,
    tagging_rules: Dict[str, Any] = None,
) -> ResourceDecision:
    """Send one resource + the tagging policy to the LLM and return its decision."""
    tagging_rules = tagging_rules or {}

    logger.info(
        f"Sending resource to OpenAI-compatible endpoint: {resource.namespace}/{resource.name} ({resource.kind})"
    )

    parser = PydanticOutputParser(pydantic_object=ResourceDecision)
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    llm = ChatOpenAI(
        model=model_id,
        base_url=base_url or os.getenv("OPENAI_BASE_URL", "https://api.ai.kodekloud.com/v1"),
        api_key=api_key or os.getenv("OPENAI_API_KEY"),
        temperature=temperature,
        max_tokens=max_tokens,
    )
    chain = prompt | llm | parser

    response = chain.invoke({
        "resource_name": resource.name,
        "namespace": resource.namespace,
        "kind": resource.kind,
        "labels": json.dumps(resource.labels, indent=2),
        "annotations": json.dumps(resource.annotations, indent=2),
        "cpu_request": resource.cpu_request,
        "memory_request": resource.memory_request,
        "replicas": resource.replicas,
        "pvc_names": resource.pvc_names,
        "pvc_size_gb": resource.pvc_size_gb,
        "is_orphaned": resource.is_orphaned,
        "tagging_rules": json.dumps(tagging_rules, indent=2),
        "format_instructions": parser.get_format_instructions(),
    })

    logger.info(f"LLM decision for {resource.namespace}/{resource.name}: {response.category}")
    return response


def generate_summary_report(results: List[Tuple[K8sResource, ResourceDecision]]) -> str:
    """Generate a human-readable summary report from (resource, decision) pairs."""
    total = len(results)
    compliant = [r for r, d in results if d.is_compliant]
    violations = [(r, d) for r, d in results if not d.is_compliant]

    compliant_count = len(compliant)
    violation_count = len(violations)
    compliant_pct = round((compliant_count / total * 100) if total else 0, 1)
    violation_pct = round((violation_count / total * 100) if total else 0, 1)

    breakdown: Dict[str, int] = {}
    for _, d in results:
        breakdown[d.category] = breakdown.get(d.category, 0) + 1

    report = f"""# FinOps Analysis Report (LLM Powered - OpenAI-Compatible)

## Tagging Summary
- **Total Resources**: {total}
- **Properly Tagged**: {compliant_count} ({compliant_pct}%)
- **Violations**: {violation_count} ({violation_pct}%)

## Breakdown by Category
"""

    for category, count in breakdown.items():
        report += f"- **{category.capitalize()}**: {count} resources\n"

    report += f"\n## Violations Found: {violation_count}\n\n"

    for i, (resource, decision) in enumerate(violations, 1):
        report += f"""### {i}. {resource.namespace}/{resource.name} ({resource.kind})
- **Category**: {decision.category}
- **Missing Tags**: {', '.join(decision.missing_tags) if decision.missing_tags else 'None'}
- **Reason**: {decision.reason}
- **Suggested Issue**: {decision.issue_title} (priority: {decision.priority})

"""

    return report
