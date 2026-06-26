from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.models import IssueCreate, IssueRecord, IssueUpdate
from app.store import IssueStore

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="FinOps Issue Tracker",
    version="1.0.0",
    description="A simple Jira-style Kanban board for FinOps findings.",
)

store = IssueStore()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
def home() -> HTMLResponse:
    return HTMLResponse((STATIC_DIR / "index.html").read_text())


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "issues": len(store.list_issues())}


@app.get("/api/issues")
def list_issues() -> dict:
    return {
        "items": [issue.model_dump(mode="json") for issue in store.list_issues()],
        "stats": store.stats(),
    }


@app.get("/issue/{issue_id}")
def get_issue(issue_id: int) -> dict:
    issue = store.get_issue(issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue.model_dump(mode="json")


@app.post(
    "/create-issue",
    response_model=IssueRecord,
    summary="Create an issue",
    description=(
        "Send a JSON payload with the issue title, summary, body, namespace, resource details, "
        "category, priority, cost impact, assignee, suggested owner, suggested cost center, labels, "
        "reasoning, and source. Returns the stored issue with an id, FINOPS key, status, and timestamps."
    ),
)
@app.post("/issue", response_model=IssueRecord, include_in_schema=False)
@app.post("/raise-issue", response_model=IssueRecord, include_in_schema=False)
def create_issue(payload: IssueCreate) -> IssueRecord:
    return store.create_issue(payload)


@app.patch("/issue/{issue_id}", response_model=IssueRecord)
def update_issue(issue_id: int, payload: IssueUpdate) -> IssueRecord:
    issue = store.update_issue(issue_id, payload)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue
