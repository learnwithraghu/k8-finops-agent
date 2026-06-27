"""Data collection, LLM structured analysis, and Tracker Integration."""
import asyncio
import json
import logging
import os
from contextlib import AsyncExitStack
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Literal

import yaml
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

try:
    from mcp import ClientSession
except ImportError:
    from mcp.client.session import ClientSession
from mcp.client.sse import sse_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Models ---
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

# --- Collection ---
RESOURCE_TYPES = ("deployments", "pods", "services", "pvc", "configmaps")

def _decode(response: Any) -> Dict[str, Any]:
    content = getattr(response, "content", None)
    if content:
        text = "".join(getattr(item, "text", "") for item in content if getattr(item, "type", None) == "text").strip()
        if text:
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                pass
    return {"items": []}

async def collect_snapshot() -> dict:
    mcp_url = os.getenv("K8S_MCP_URL", "http://localhost:8000/sse")
    async with AsyncExitStack() as stack:
        logger.info(f"Connecting to Kubernetes MCP server at {mcp_url}...")
        read_stream, write_stream = await stack.enter_async_context(sse_client(mcp_url))
        session = await stack.enter_async_context(ClientSession(read_stream, write_stream))
        await session.initialize()
        
        payload = _decode(await session.call_tool("kubectl_get", {"namespace": "", "resourceType": "namespaces"}))
        namespaces = [item["name"] for item in payload.get("items", []) if item.get("name")]
        
        resources = []
        for ns in namespaces:
            if ns.startswith("kube-") or ns == "local-path-storage":
                continue
            for r_type in RESOURCE_TYPES:
                resp = await session.call_tool("kubectl_get", {"namespace": ns, "resourceType": r_type})
                items = _decode(resp).get("items", [])
                for item in items:
                    item.pop("annotations", None)
                resources.extend(items)

        resources.sort(key=lambda item: (item.get("namespace", ""), item.get("kind", ""), item.get("name", "")))
        return {
            "scanned_at": datetime.now(timezone.utc).isoformat(),
            "cluster": "kind",
            "namespaces": namespaces,
            "resources": resources
        }

# --- Analysis ---
def analyze_snapshot(snapshot: dict, tagging_rules: dict) -> TicketBatch:
    logger.info("Sending %s resources to LLM", len(snapshot.get("resources", [])))
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL_ID", "gpt-4o"),
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.ai.kodekloud.com/v1"),
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.2, max_tokens=2048,
    )
    sys_prompt = "You are a FinOps assistant. Return ONLY JSON matching schema: {\"tickets\": [TrackerTicket, ...]}"
    prompt = (
        f"Snapshot:\n{json.dumps(snapshot)}\n\nRules:\n{yaml.safe_dump(tagging_rules)}\n"
        "- If an orphaned PVC, or missing cost-center, or no owner, create a ticket.\n"
        "- If all required tags present, do not create a ticket.\n"
    )
    response = llm.invoke([("system", sys_prompt), ("human", prompt)])
    content = str(getattr(response, "content", response)).strip("` \n")
    if content.startswith("json"): content = content[4:].strip()
    return TicketBatch.model_validate_json(content)

# --- Integration ---
async def post_tickets(batch: TicketBatch):
    logger.info(f"Posting {len(batch.tickets)} tickets to Issue Tracker via MCP...")
    tracker_url = os.getenv("TRACKER_MCP_URL", "http://localhost:8086/sse")
    
    async with sse_client(tracker_url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            for i, ticket in enumerate(batch.tickets):
                logger.info(f"Creating ticket {i+1}/{len(batch.tickets)}: {ticket.title}")
                await session.call_tool("create_issue", ticket.model_dump())

async def main():
    # 1. Collect
    snapshot = await collect_snapshot()
    
    # 2. Analyze
    rules_path = Path(__file__).parents[1] / "07-llm-structured-agent" / "config" / "tagging-rules.yaml"
    rules = yaml.safe_load(rules_path.read_text()) if rules_path.exists() else {}
    batch = analyze_snapshot(snapshot, rules)
    print(f"\n--- FOUND {len(batch.tickets)} ISSUES ---")
    
    # 3. Post
    await post_tickets(batch)
    print("\n--- ALL ISSUES POSTED TO TRACKER ---")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parents[2] / ".env")
    asyncio.run(main())
