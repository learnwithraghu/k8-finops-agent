"""MCP client for the Section 08 issue tracker service.

Connects to the tracker's MCP server and calls the create_issue tool
to create tickets from LLM decisions.
"""

import asyncio
import logging
from typing import Any, Dict, List

from mcp import ClientSession
from mcp.client.sse import sse_client

from agent.analyzer import ResourceDecision
from agent.scanner import K8sResource

logger = logging.getLogger(__name__)


class IssueTrackerClient:
    """MCP client for the local FinOps issue tracker."""

    def __init__(self, mcp_url: str = "http://localhost:8086/mcp"):
        self.mcp_url = mcp_url

    async def connect(self) -> bool:
        """Confirm the MCP server is reachable."""
        try:
            async with sse_client(self.mcp_url) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    tools = await session.list_tools()
                    logger.info(
                        f"Connected to issue tracker MCP server, {len(tools.tools)} tools available"
                    )
                    return True
        except Exception as exc:
            logger.error(f"Failed to connect to issue tracker MCP server: {exc}")
            return False

    async def create_issue(
        self, resource: K8sResource, decision: ResourceDecision
    ) -> Dict[str, Any]:
        """Create one issue via MCP tool call."""
        arguments = {
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
            "reasoning": decision.reason,
            "source": "mcp-llm-agent",
        }

        async with sse_client(self.mcp_url) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool("create_issue", arguments)
                if result.content:
                    import json

                    return json.loads(result.content[0].text)
                return {}

    async def create_issues(
        self,
        results: List[tuple[K8sResource, ResourceDecision]],
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Create tracker issues for every actionable decision."""
        created: List[Dict[str, Any]] = []
        failed: List[Dict[str, Any]] = []

        for resource, decision in results:
            try:
                issue = await self.create_issue(resource, decision)
                created.append(issue)
                logger.info(
                    f"Created tracker issue for {resource.namespace}/{resource.name}"
                )
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

    def create_issues_sync(
        self, results: List[tuple[K8sResource, ResourceDecision]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Synchronous wrapper for create_issues."""
        return asyncio.run(self.create_issues(results))
