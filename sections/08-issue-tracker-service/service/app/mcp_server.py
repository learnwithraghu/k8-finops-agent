from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp.server.fastmcp import FastMCP

from app.models import IssueCreate, IssueUpdate
from app.store import IssueStore

store = IssueStore()

mcp = FastMCP(
    "finops-issue-tracker",
    instructions="Issue tracker for FinOps findings. Create, list, get, and update issues.",
)


@mcp.tool()
def create_issue(
    title: str,
    summary: str = "",
    body: str = "",
    namespace: str = "",
    resource_name: str = "",
    resource_kind: str = "",
    category: str = "",
    priority: str = "medium",
    cost_impact: float = 0.0,
    assignee: str = "",
    suggested_owner: str = "",
    suggested_cost_center: str = "",
    reasoning: str = "",
    source: str = "mcp-agent",
) -> dict:
    payload = IssueCreate(
        title=title,
        summary=summary,
        body=body,
        namespace=namespace,
        resource_name=resource_name,
        resource_kind=resource_kind,
        category=category,
        priority=priority,
        cost_impact=cost_impact,
        assignee=assignee,
        suggested_owner=suggested_owner,
        suggested_cost_center=suggested_cost_center,
        reasoning=reasoning,
        source=source,
    )
    issue = store.create_issue(payload)
    return issue.model_dump(mode="json")


@mcp.tool()
def list_issues() -> dict:
    items = [issue.model_dump(mode="json") for issue in store.list_issues()]
    return {"items": items, "stats": store.stats()}


@mcp.tool()
def get_issue(issue_id: int) -> dict:
    issue = store.get_issue(issue_id)
    if not issue:
        return {"error": "Issue not found"}
    return issue.model_dump(mode="json")


@mcp.tool()
def update_issue(
    issue_id: int, status: str | None = None, assignee: str | None = None
) -> dict:
    payload = IssueUpdate(status=status, assignee=assignee)
    issue = store.update_issue(issue_id, payload)
    if not issue:
        return {"error": "Issue not found"}
    return issue.model_dump(mode="json")


def main() -> None:
    import uvicorn

    app = mcp.sse_app()
    uvicorn.run(app, host="0.0.0.0", port=8001)


if __name__ == "__main__":
    main()
