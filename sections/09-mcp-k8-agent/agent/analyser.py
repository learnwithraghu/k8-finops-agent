"""LLM compliance analysis for raw MCP cluster snapshots."""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, List

import yaml
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from pydantic import BaseModel

from agent.models import ClusterSnapshot, ComplianceReport, ResourceAssessment

logger = logging.getLogger(__name__)


class AssessmentBundle(BaseModel):
    """Top-level parser model for the LLM output."""

    assessments: List[ResourceAssessment]


SYSTEM_PROMPT = """You are a FinOps compliance analyser for a Kubernetes-based airline platform.

Your job is to inspect a raw cluster snapshot, apply the tagging policy carefully, and return one assessment per resource.

Do not create Jira fields or suggest tracker workflow steps.
Return only structured JSON that matches the parser schema.
"""

USER_PROMPT = """Cluster snapshot:
{cluster_snapshot}

Tagging policy:
{tagging_rules}

{format_instructions}

Rules:
- Match labels against required_tags and label_mappings.
- If a resource is an orphaned PVC, it is never compliant.
- If a resource is missing cost-center, category must be "unallocated".
- If a resource has cost-center but no owner, category must be "unowned".
- If a resource has no labels and lives in the default namespace, category must be "unknown".
- If all required tags are present, category must be "tagged" and is_compliant must be true.
- Keep reason concise, specific, and actionable.
- Use concrete values for suggested_owner, suggested_cost_center, and suggested_tags.
"""


def analyze_snapshot(
    snapshot: ClusterSnapshot,
    tagging_rules: Dict[str, Any],
    model_id: str,
    base_url: str | None = None,
    api_key: str | None = None,
    max_tokens: int = 2048,
    temperature: float = 0.2,
) -> ComplianceReport:
    """Send the full snapshot and policy to the LLM and return a structured report."""

    logger.info("Sending %s resources to the LLM analyst", len(snapshot.resources))

    parser = PydanticOutputParser(pydantic_object=AssessmentBundle)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", USER_PROMPT),
        ]
    )
    llm = ChatOpenAI(
        model=model_id,
        base_url=base_url or os.getenv("OPENAI_BASE_URL", "https://api.ai.kodekloud.com/v1"),
        api_key=api_key or os.getenv("OPENAI_API_KEY"),
        temperature=temperature,
        max_tokens=max_tokens,
    )
    chain = prompt | llm | parser

    response = chain.invoke(
        {
            "cluster_snapshot": json.dumps(snapshot.model_dump(), indent=2),
            "tagging_rules": yaml.safe_dump(tagging_rules, sort_keys=False),
            "format_instructions": parser.get_format_instructions(),
        }
    )

    assessments_raw = response.assessments if hasattr(response, "assessments") else response["assessments"]
    assessments = [
        item if isinstance(item, ResourceAssessment) else ResourceAssessment.model_validate(item)
        for item in assessments_raw
    ]
    compliant_count = sum(1 for item in assessments if item.is_compliant)
    violation_count = len(assessments) - compliant_count

    return ComplianceReport(
        scanned_at=snapshot.scanned_at,
        cluster=snapshot.cluster,
        total_resources=len(snapshot.resources),
        compliant_count=compliant_count,
        violation_count=violation_count,
        assessments=assessments,
    )
