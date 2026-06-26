"""LLM analysis for raw MCP cluster snapshots."""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict

import yaml
from langchain_openai import ChatOpenAI

from agent.models import TicketBatch

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a FinOps assistant for a Kubernetes-based airline platform.

Read the cluster snapshot and tagging policy.
Return only JSON matching this schema:
{"tickets": [{"title": "...", "summary": "...", "body": "...", "namespace": "...", "resource_name": "...", "resource_kind": "...", "category": "...", "priority": "high", "cost_impact": 0.0, "assignee": "...", "suggested_owner": "...", "suggested_cost_center": "...", "labels": ["..."], "reasoning": "...", "source": "mcp-llm-agent"}]}

Create ticket objects only for resources that need action.
Each ticket must be ready to POST to /create-issue with no extra transformation.
"""


def analyze_snapshot(
    snapshot: Dict[str, Any],
    tagging_rules: Dict[str, Any],
    model_id: str,
    base_url: str | None = None,
    api_key: str | None = None,
    max_tokens: int = 2048,
    temperature: float = 0.2,
) -> TicketBatch:
    logger.info("Sending %s resources to the LLM analyst", len(snapshot.get("resources", [])))

    llm = ChatOpenAI(
        model=model_id,
        base_url=base_url or os.getenv("OPENAI_BASE_URL", "https://api.ai.kodekloud.com/v1"),
        api_key=api_key or os.getenv("OPENAI_API_KEY"),
        temperature=temperature,
        max_tokens=max_tokens,
    )
    prompt = (
        f"Cluster snapshot:\n{json.dumps(snapshot, indent=2)}\n\n"
        f"Tagging policy:\n{yaml.safe_dump(tagging_rules, sort_keys=False)}\n\n"
        "Rules:\n"
        "- Match labels against required_tags and label_mappings.\n"
        "- If a resource is an orphaned PVC, create a ticket.\n"
        "- If a resource is missing cost-center, create a ticket.\n"
        "- If a resource has cost-center but no owner, create a ticket.\n"
        "- If a resource has no labels and lives in the default namespace, create a ticket.\n"
        "- If all required tags are present, do not create a ticket.\n"
        "- Keep summary and reasoning short.\n"
        "- Fill in suggested_owner, suggested_cost_center, and suggested_tags with concrete values.\n"
        "- Make labels useful for triage.\n"
    )
    response = llm.invoke([("system", SYSTEM_PROMPT), ("human", prompt)])

    content = str(response.content if hasattr(response, "content") else response).strip()
    if content.startswith("```"):
        content = content.strip("`").strip()
        if content.startswith("json"):
            content = content[4:].strip()
    return TicketBatch.model_validate_json(content)
