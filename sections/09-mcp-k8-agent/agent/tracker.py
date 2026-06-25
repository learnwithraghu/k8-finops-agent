"""Issue tracker client for the Section 09 MCP FinOps pipeline."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, List

import requests

from agent.models import AnalysisEnvelope, ComplianceReport, ResourceAssessment, ResourceSnapshot

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TrackerIssue:
    title: str
    summary: str
    body: str
    namespace: str
    resource_name: str
    resource_kind: str
    category: str
    priority: str
    suggested_owner: str
    suggested_cost_center: str
    labels: List[str]
    reasoning: str
    source: str = "mcp-llm-agent"
    cost_impact: float = 0.0
    assignee: str = ""


class IssueTrackerClient:
    """Small client for the local issue tracker service."""

    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def connect(self) -> bool:
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=self.timeout)
            response.raise_for_status()
            logger.info("Connected to issue tracker at %s", self.base_url)
            return True
        except Exception as exc:
            logger.error("Failed to connect to issue tracker at %s: %s", self.base_url, exc)
            return False

    def build_issue(
        self,
        snapshot: ResourceSnapshot,
        assessment: ResourceAssessment,
        report: ComplianceReport,
    ) -> TrackerIssue:
        title = f"[FinOps] {assessment.namespace}/{assessment.name} - {assessment.category.upper()}"
        summary = assessment.reason
        body = self._build_body(snapshot, assessment, report)
        labels = ["finops", assessment.category, assessment.priority]
        if snapshot.kind not in labels:
            labels.append(snapshot.kind.lower())

        return TrackerIssue(
            title=title,
            summary=summary,
            body=body,
            namespace=assessment.namespace,
            resource_name=assessment.name,
            resource_kind=assessment.kind,
            category=assessment.category,
            priority=assessment.priority,
            suggested_owner=assessment.suggested_owner,
            suggested_cost_center=assessment.suggested_cost_center,
            labels=labels,
            reasoning=assessment.reason,
            assignee=assessment.suggested_owner if assessment.suggested_owner else "",
        )

    def create_issue(self, issue: TrackerIssue) -> Dict[str, object]:
        payload = self._payload(issue)
        response = self.session.post(
            f"{self.base_url}/create-issue",
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def create_from_envelope(self, envelope: AnalysisEnvelope) -> Dict[str, object]:
        resources = {
            (item.kind, item.namespace, item.name): item
            for item in envelope.snapshot.resources
        }

        created: List[Dict[str, object]] = []
        failed: List[Dict[str, object]] = []
        skipped: List[str] = []

        for assessment in envelope.report.assessments:
            if assessment.is_compliant:
                skipped.append(f"{assessment.namespace}/{assessment.name}")
                continue

            snapshot = resources.get((assessment.kind, assessment.namespace, assessment.name))
            if snapshot is None:
                failed.append(
                    {
                        "resource": f"{assessment.namespace}/{assessment.name}",
                        "error": "No matching resource snapshot found",
                    }
                )
                continue

            try:
                issue = self.build_issue(snapshot, assessment, envelope.report)
                result = self.create_issue(issue)
                created.append(result)
                logger.info("Created tracker issue for %s/%s", assessment.namespace, assessment.name)
            except Exception as exc:
                logger.error("Failed to create issue for %s/%s: %s", assessment.namespace, assessment.name, exc)
                failed.append(
                    {
                        "resource": f"{assessment.namespace}/{assessment.name}",
                        "title": assessment.reason,
                        "error": str(exc),
                    }
                )

        return {"created": created, "failed": failed, "skipped": skipped}

    def _payload(self, issue: TrackerIssue) -> Dict[str, object]:
        return {
            "title": issue.title,
            "summary": issue.summary,
            "body": issue.body,
            "namespace": issue.namespace,
            "resource_name": issue.resource_name,
            "resource_kind": issue.resource_kind,
            "category": issue.category,
            "priority": issue.priority,
            "cost_impact": issue.cost_impact,
            "assignee": issue.assignee,
            "suggested_owner": issue.suggested_owner,
            "suggested_cost_center": issue.suggested_cost_center,
            "labels": issue.labels,
            "reasoning": issue.reasoning,
            "source": issue.source,
        }

    def _build_body(self, snapshot: ResourceSnapshot, assessment: ResourceAssessment, report: ComplianceReport) -> str:
        return (
            f"## Resource\n"
            f"- Kind: {snapshot.kind}\n"
            f"- Namespace: {snapshot.namespace}\n"
            f"- Name: {snapshot.name}\n\n"
            f"## Compliance\n"
            f"- Category: {assessment.category}\n"
            f"- Priority: {assessment.priority}\n"
            f"- Missing tags: {', '.join(assessment.missing_tags) if assessment.missing_tags else 'None'}\n"
            f"- Reason: {assessment.reason}\n\n"
            f"## Suggested remediation\n"
            f"- Suggested owner: {assessment.suggested_owner or 'unknown'}\n"
            f"- Suggested cost center: {assessment.suggested_cost_center or 'unknown'}\n"
            f"- Suggested tags: {assessment.suggested_tags}\n\n"
            f"## Scan context\n"
            f"- Scanned at: {report.scanned_at}\n"
            f"- Cluster: {report.cluster}\n"
        )
