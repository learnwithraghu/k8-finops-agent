"""Minimal client for the Section 09 issue tracker service.

Converts LLM decisions (ResourceDecision + K8sResource) into tracker payloads
and POSTs them to the local FastAPI service.
"""

import logging
from typing import Any, Dict, List

import requests

from agent.analyzer import ResourceDecision
from agent.scanner import K8sResource

logger = logging.getLogger(__name__)


class IssueTrackerClient:
    """Small client for the local FinOps issue tracker."""

    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def connect(self) -> bool:
        """Confirm the tracker is running before sending issues."""
        try:
            response = self.session.get(
                f"{self.base_url}/health", timeout=self.timeout
            )
            response.raise_for_status()
            logger.info(f"Connected to issue tracker at {self.base_url}")
            return True
        except Exception as exc:
            logger.error(
                f"Failed to connect to issue tracker at {self.base_url}: {exc}"
            )
            return False

    def build_payload(
        self, resource: K8sResource, decision: ResourceDecision
    ) -> Dict[str, Any]:
        """Map a resource + LLM decision to the tracker IssueCreate schema."""
        return {
            "title": decision.issue_title,
            "summary": decision.reason,
            "body": decision.issue_body,
            "namespace": resource.namespace,
            "resource_name": resource.name,
            "resource_kind": resource.kind,
            "category": decision.category,
            "priority": decision.priority,
            "cost_impact": 0.0,
            "assignee": decision.suggested_owner
            if decision.suggested_owner and decision.suggested_owner != "unknown"
            else "",
            "suggested_owner": decision.suggested_owner,
            "suggested_cost_center": decision.suggested_cost_center,
            "labels": decision.issue_labels,
            "reasoning": decision.reason,
            "source": "llm-agent",
        }

    def create_issue(
        self, resource: K8sResource, decision: ResourceDecision
    ) -> Dict[str, Any]:
        """Create one issue in the tracker."""
        payload = self.build_payload(resource, decision)

        response = self.session.post(
            f"{self.base_url}/create-issue",
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def create_issues(
        self,
        results: List[tuple[K8sResource, ResourceDecision]],
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Create tracker issues for every actionable decision."""
        created: List[Dict[str, Any]] = []
        failed: List[Dict[str, Any]] = []

        for resource, decision in results:
            try:
                issue = self.create_issue(resource, decision)
                created.append(issue)
                logger.info(f"Created tracker issue for {resource.namespace}/{resource.name}")
            except Exception as exc:
                logger.error(
                    f"Failed to create issue for {resource.namespace}/{resource.name}: {exc}"
                )
                failed.append(
                    {
                        "resource": f"{resource.namespace}/{resource.name}",
                        "title": decision.issue_title,
                        "error": str(exc),
                    }
                )

        return {"created": created, "failed": failed}
