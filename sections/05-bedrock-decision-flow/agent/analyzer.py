"""AWS Bedrock AI analyzer for FinOps agent using LangChain."""

import json
import logging
from dataclasses import dataclass
from typing import Dict, Any, List

from pydantic import BaseModel, Field
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from agent.scanner import K8sResource
from agent.tagging_violations import TaggingViolation

logger = logging.getLogger(__name__)


class IssueDraftResponse(BaseModel):
    """Pydantic model for structured LLM output."""
    should_create_issue: bool = Field(description="Whether to create an issue for this resource")
    issue_title: str = Field(description="GitHub issue title in format: [FinOps] namespace/name - CATEGORY")
    issue_body: str = Field(description="Markdown body with summary, missing tags, and remediation steps")
    issue_labels: List[str] = Field(description="GitHub issue labels")
    priority: str = Field(description="Priority level: critical, high, medium, or low")
    reasoning: str = Field(description="Short explanation for the decision")
    suggested_cost_center: str = Field(description="Suggested cost center for the resource")
    suggested_owner: str = Field(description="Suggested team owner for the resource")
    suggested_tags: Dict[str, str] = Field(description="Suggested tags to apply")


@dataclass
class IssueDraft:
    """Bedrock-generated GitHub issue payload."""
    title: str
    body: str
    labels: List[str]
    priority: str
    should_create_issue: bool
    reasoning: str
    suggested_cost_center: str
    suggested_owner: str
    suggested_tags: Dict[str, str]


PROMPT_TEMPLATE = """You are a FinOps agent for a Kubernetes-based airline platform.

Review the following resource and produce a GitHub issue draft.
Return ONLY valid JSON that matches the required schema.

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
- Category: {category}
- Missing Tags: {missing_tags}
- Reason: {reason}

Tagging Policy:
{tagging_rules}

{format_instructions}

Rules:
- Use the tagging policy and airline context.
- Prefer concrete team names.
- Set should_create_issue=false only if this is clearly not actionable.
- Keep titles concise.
- Body should include: summary, missing tags, and remediation steps.
"""


def analyze_resource(
    resource: K8sResource,
    violation: TaggingViolation,
    model_id: str,
    region: str = "us-east-1",
    max_tokens: int = 1024,
    temperature: float = 0.3,
    tagging_rules: Dict[str, Any] = None,
) -> IssueDraft:
    """Analyze a resource and return a GitHub issue draft using LangChain."""
    tagging_rules = tagging_rules or {}

    logger.info(
        f"Sending resource to Bedrock: {resource.namespace}/{resource.name} ({resource.kind})"
    )

    parser = PydanticOutputParser(pydantic_object=IssueDraftResponse)
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    llm = ChatBedrock(
        model_id=model_id,
        region_name=region,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    chain = prompt | llm | parser

    try:
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
            "category": violation.category.value,
            "missing_tags": ', '.join(str(t) for t in violation.missing_tags if t) if violation.missing_tags else 'None',
            "reason": violation.reason,
            "tagging_rules": json.dumps(tagging_rules, indent=2),
            "format_instructions": parser.get_format_instructions(),
        })

        logger.info(f"Bedrock analysis complete for {resource.namespace}/{resource.name}")

        return IssueDraft(
            title=response.issue_title,
            body=response.issue_body,
            labels=list(dict.fromkeys(response.issue_labels)),
            priority=response.priority,
            should_create_issue=response.should_create_issue,
            reasoning=response.reasoning,
            suggested_cost_center=response.suggested_cost_center,
            suggested_owner=response.suggested_owner,
            suggested_tags=response.suggested_tags,
        )
    except Exception as e:
        logger.exception(f"Error invoking LangChain chain: {e}")
        raise


def analyze_batch(
    violations: List[TaggingViolation],
    model_id: str,
    region: str = "us-east-1",
    max_tokens: int = 1024,
    temperature: float = 0.3,
    tagging_rules: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """Analyze multiple violations and return summary."""
    results = []

    for violation in violations:
        draft = analyze_resource(
            violation.resource, violation, model_id, region, max_tokens, temperature, tagging_rules
        )
        results.append({
            'resource': f"{violation.resource.namespace}/{violation.resource.name}",
            'kind': violation.resource.kind,
            'issue': {
                'title': draft.title,
                'priority': draft.priority,
                'should_create_issue': draft.should_create_issue,
                'reasoning': draft.reasoning,
                'labels': draft.labels,
            }
        })

    return {
        'analyzed_count': len(violations),
        'recommendations': results,
    }


def generate_summary_report(violations_analysis: Dict[str, Any]) -> str:
    """Generate a human-readable summary report."""
    report = f"""# FinOps Analysis Report (LLM Powered - Bedrock)

## Tagging Summary
- **Total Resources**: {violations_analysis['total_resources']}
- **Properly Tagged**: {violations_analysis['properly_tagged']} ({violations_analysis['tagged_percentage']}%)
- **Violations**: {violations_analysis['violations']} ({violations_analysis['violation_percentage']}%)

## Breakdown by Category
"""

    for category, count in violations_analysis.get('breakdown_by_category', {}).items():
        report += f"- **{category.capitalize()}**: {count} resources\n"

    report += f"\n## Violations Found: {len(violations_analysis.get('violations_list', []))}\n\n"

    for i, v in enumerate(violations_analysis.get('violations_list', []), 1):
        report += f"""### {i}. {v['resource']} ({v['kind']})
- **Category**: {v['category']}
- **Missing Tags**: {', '.join(str(t) for t in v['missing_tags'] if t) if v['missing_tags'] else 'None'}
- **Reason**: {v['reason']}

"""

    return report