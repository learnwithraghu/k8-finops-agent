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


MCP_LANDING_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>FinOps Issue Tracker MCP</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 720px; margin: 40px auto; padding: 0 20px; color: #0f172a; }
    p, li { line-height: 1.5; color: #475569; }
    code { background: #f1f5f9; padding: 2px 6px; border-radius: 6px; }
    a { color: #2563eb; }
    .note { background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 10px; padding: 14px 16px; }
  </style>
</head>
<body>
  <h1>MCP transport (port 8086)</h1>
  <p class="note">
    This port is for <strong>agents</strong>, not a browser UI.
    A <code>GET /</code> returns this page; tool calls go over SSE at <code>/sse</code>.
  </p>
  <h2>Endpoints</h2>
  <ul>
    <li><code>GET /sse</code> — agent connection (long-lived stream)</li>
    <li><code>POST /messages/</code> — tool invocations from the agent client</li>
  </ul>
  <h2>Human-friendly docs</h2>
  <ul>
    <li><a href="http://localhost:8085/">Kanban board</a> (port 8085)</li>
    <li><a href="http://localhost:8085/docs">REST Swagger</a> (port 8085)</li>
    <li><code>python3 sections/08-from-findings-to-tickets/agent/list_tracker_tools.py</code></li>
  </ul>
</body>
</html>"""


def build_app():
    from starlette.applications import Starlette
    from starlette.responses import HTMLResponse
    from starlette.routing import Mount, Route

    async def landing(_request):
        return HTMLResponse(MCP_LANDING_HTML)

    return Starlette(
        routes=[
            Route("/", landing),
            Mount("/", app=mcp.sse_app()),
        ]
    )


def main() -> None:
    import uvicorn

    uvicorn.run(build_app(), host="0.0.0.0", port=8001)


if __name__ == "__main__":
    main()
