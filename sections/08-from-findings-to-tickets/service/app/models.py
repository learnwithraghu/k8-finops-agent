from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Priority(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"


class Status(str, Enum):
    backlog = "backlog"
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class IssueCreate(BaseModel):
    title: str
    summary: str = ""
    body: str = ""
    namespace: str = ""
    resource_name: str = ""
    resource_kind: str = ""
    category: str = ""
    priority: Priority = Priority.medium
    cost_impact: float = 0.0
    assignee: str = ""
    suggested_owner: str = ""
    suggested_cost_center: str = ""
    labels: List[str] = Field(default_factory=list)
    reasoning: str = ""
    source: str = "bedrock"


class IssueUpdate(BaseModel):
    status: Optional[Status] = None
    assignee: Optional[str] = None


class IssueRecord(IssueCreate):
    id: int
    key: str
    status: Status = Status.backlog
    created_at: str
    updated_at: str

    @classmethod
    def from_create(cls, issue_id: int, payload: IssueCreate) -> "IssueRecord":
        now = datetime.now(timezone.utc).isoformat()
        return cls(
            id=issue_id,
            key=f"FINOPS-{issue_id:04d}",
            status=Status.backlog,
            created_at=now,
            updated_at=now,
            **payload.model_dump(),
        )

    def touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc).isoformat()
