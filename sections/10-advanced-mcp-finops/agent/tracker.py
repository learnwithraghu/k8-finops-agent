"""Tiny tracker handoff for the Section 09 MCP FinOps demo."""

from __future__ import annotations

import logging
from typing import Dict, List

import requests

logger = logging.getLogger(__name__)


def post_tickets(base_url: str, tickets: List[object], timeout: int = 10) -> Dict[str, object]:
    session = requests.Session()
    created: List[Dict[str, object]] = []
    failed: List[Dict[str, object]] = []
    base_url = base_url.rstrip("/")

    for ticket in tickets:
        payload = ticket.model_dump() if hasattr(ticket, "model_dump") else dict(ticket)
        try:
            response = session.post(f"{base_url}/create-issue", json=payload, timeout=timeout)
            response.raise_for_status()
            created.append(response.json())
        except Exception as exc:
            logger.error("Failed to create ticket %s: %s", payload.get("title", "<unknown>"), exc)
            failed.append({"ticket": payload.get("title", "<unknown>"), "error": str(exc)})

    return {"created": created, "failed": failed, "tracker_available": True}
