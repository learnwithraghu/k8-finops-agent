"""Minimal models for the Section 09 MCP FinOps demo."""

from typing import Dict, List, Literal

from pydantic import BaseModel, Field


class TrackerTicket(BaseModel):
    title: str
    summary: str = ""
    body: str = ""
    namespace: str = ""
    resource_name: str = ""
    resource_kind: str = ""
    category: str = ""
    priority: Literal["critical", "high", "medium", "low"] = "medium"
    cost_impact: float = 0.0
    assignee: str = ""
    suggested_owner: str = ""
    suggested_cost_center: str = ""
    labels: List[str] = Field(default_factory=list)
    reasoning: str = ""
    source: str = "mcp-llm-agent"


class TicketBatch(BaseModel):
    tickets: List[TrackerTicket] = Field(default_factory=list)
