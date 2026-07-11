"""Deterministic MCP collection → structured JSON snapshot with labels."""
import asyncio
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pydantic import BaseModel, Field

from mcp_client import decode_tool_result, get_mcp_tools, tool_by_name

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RESOURCE_TYPES = ("deployments", "pods", "services", "pvc", "configmaps")


class ClusterSnapshot(BaseModel):
    scanned_at: str
    cluster: str = "kind"
    namespaces: list[str]
    resources: list[dict[str, Any]] = Field(default_factory=list)


async def collect_snapshot() -> ClusterSnapshot:
    tools, cleanup = await get_mcp_tools()
    try:
        kubectl_get = tool_by_name(tools, "kubectl_get")

        logger.info("Fetching namespaces...")
        payload = decode_tool_result(
            await kubectl_get.ainvoke({"namespace": "", "resourceType": "namespaces"})
        )
        namespaces = [item["name"] for item in payload.get("items", []) if item.get("name")]

        resources: list[dict[str, Any]] = []
        for ns in namespaces:
            if ns.startswith("kube-") or ns == "local-path-storage":
                continue

            logger.info("Scanning namespace: %s", ns)
            for resource_type in RESOURCE_TYPES:
                items = decode_tool_result(
                    await kubectl_get.ainvoke({"namespace": ns, "resourceType": resource_type})
                ).get("items", [])
                for item in items:
                    item.pop("annotations", None)
                resources.extend(items)

        resources.sort(
            key=lambda item: (item.get("namespace", ""), item.get("kind", ""), item.get("name", ""))
        )
        return ClusterSnapshot(
            scanned_at=datetime.now(timezone.utc).isoformat(),
            namespaces=namespaces,
            resources=resources,
        )
    finally:
        await cleanup()


async def main() -> None:
    snapshot = await collect_snapshot()
    print(json.dumps(snapshot.model_dump(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
