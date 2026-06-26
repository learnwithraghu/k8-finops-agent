from __future__ import annotations

import json
from pathlib import Path
from threading import Lock
from typing import List, Optional

from app.models import IssueCreate, IssueRecord, IssueUpdate, Status


class IssueStore:
    def __init__(self, data_path: Optional[Path] = None):
        self.data_path = data_path or Path(__file__).resolve().parent.parent / "data" / "issues.json"
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
        self._issues: List[IssueRecord] = []
        self._load()

    def _sanitize_status(self, value: str) -> str:
        if value in {s.value for s in Status}:
            return value
        return Status.backlog.value

    def _load(self) -> None:
        if not self.data_path.exists():
            self._issues = []
            self._persist()
            return

        try:
            raw = json.loads(self.data_path.read_text())
            self._issues = []
            for item in raw:
                item = dict(item)
                item["status"] = self._sanitize_status(str(item.get("status", "backlog")))
                self._issues.append(IssueRecord.model_validate(item))
        except Exception:
            self._issues = []
            self._persist()

    def _persist(self) -> None:
        payload = [issue.model_dump(mode="json") for issue in self._issues]
        self.data_path.write_text(json.dumps(payload, indent=2))

    def list_issues(self) -> List[IssueRecord]:
        with self._lock:
            return list(self._issues)

    def get_issue(self, issue_id: int) -> Optional[IssueRecord]:
        with self._lock:
            for issue in self._issues:
                if issue.id == issue_id:
                    return issue
        return None

    def create_issue(self, payload: IssueCreate) -> IssueRecord:
        with self._lock:
            next_id = max((issue.id for issue in self._issues), default=0) + 1
            issue = IssueRecord.from_create(next_id, payload)
            self._issues.append(issue)
            self._persist()
            return issue

    def update_issue(self, issue_id: int, payload: IssueUpdate) -> Optional[IssueRecord]:
        with self._lock:
            for issue in self._issues:
                if issue.id == issue_id:
                    if payload.status is not None:
                        issue.status = payload.status
                    if payload.assignee is not None:
                        issue.assignee = payload.assignee
                    issue.touch()
                    self._persist()
                    return issue
        return None

    def stats(self) -> dict:
        with self._lock:
            return {
                "total": len(self._issues),
                "backlog": sum(1 for issue in self._issues if issue.status == Status.backlog),
                "todo": sum(1 for issue in self._issues if issue.status == Status.todo),
                "in_progress": sum(1 for issue in self._issues if issue.status == Status.in_progress),
                "done": sum(1 for issue in self._issues if issue.status == Status.done),
                "estimated_monthly_savings": round(sum(issue.cost_impact for issue in self._issues), 2),
            }
