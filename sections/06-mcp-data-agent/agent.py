"""Collect raw Kubernetes data through MCP tools."""
import asyncio
import json
import logging
import os
from contextlib import AsyncExitStack
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

try:
    from mcp import ClientSession
except ImportError:
    from mcp.client.session import ClientSession
from mcp.client.sse import sse_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# The resource types we want to fetch
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

async def main() -> None:
    mcp_url = os.getenv("K8S_MCP_URL", "http://localhost:8000/sse")
    async with AsyncExitStack() as stack:
        logger.info(f"Connecting to Kubernetes MCP server at {mcp_url}...")
        read_stream, write_stream = await stack.enter_async_context(sse_client(mcp_url))
        session = await stack.enter_async_context(ClientSession(read_stream, write_stream))
        await session.initialize()
        
        logger.info("Fetching namespaces...")
        payload = _decode(await session.call_tool("kubectl_get", {"namespace": "", "resourceType": "namespaces"}))
        namespaces = [item["name"] for item in payload.get("items", []) if item.get("name")]
        
        resources: List[Dict[str, Any]] = []
        for ns in namespaces:
            # Skip system namespaces to keep payload small
            if ns.startswith("kube-") or ns == "local-path-storage":
                continue
                
            logger.info(f"Scanning namespace: {ns}")
            for r_type in RESOURCE_TYPES:
                response = await session.call_tool("kubectl_get", {"namespace": ns, "resourceType": r_type})
                items = _decode(response).get("items", [])
                for item in items:
                    item.pop("annotations", None)
                resources.extend(items)

        resources.sort(key=lambda item: (item.get("namespace", ""), item.get("kind", ""), item.get("name", "")))
        
        snapshot = {
            "scanned_at": datetime.now(timezone.utc).isoformat(),
            "cluster": "kind",
            "namespaces": namespaces,
            "resources": resources
        }
        
        print(json.dumps(snapshot, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
