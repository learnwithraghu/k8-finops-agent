"""Deterministic collector that reads Kubernetes data through MCP tools."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import shlex
import sys
from contextlib import AsyncExitStack
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence

try:
    from mcp import ClientSession
except ImportError:  # pragma: no cover - compatibility with older SDK layouts
    from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

from agent.models import ClusterSnapshot, ResourceSnapshot

logger = logging.getLogger(__name__)


class ClusterCollector:
    """Fetch raw cluster data from the MCP server and assemble a snapshot."""

    def __init__(
        self,
        namespace: Optional[str] = None,
        cluster_name: Optional[str] = None,
        server_command: Optional[Sequence[str]] = None,
        server_args: Optional[Sequence[str]] = None,
    ) -> None:
        self.namespace = namespace
        self.cluster_name = cluster_name or os.getenv("CLUSTER_NAME", "kind")
        self.server_command = list(server_command or [os.getenv("MCP_SERVER_COMMAND", sys.executable)])
        self.server_args = list(server_args or shlex.split(os.getenv("MCP_SERVER_ARGS", "-m mcp_server.server")))

    async def collect(self) -> ClusterSnapshot:
        """Collect a complete raw snapshot of the cluster."""

        server_params = StdioServerParameters(
            command=self.server_command[0],
            args=self.server_args,
            env=os.environ.copy(),
        )

        async with AsyncExitStack() as stack:
            read_stream, write_stream = await stack.enter_async_context(stdio_client(server_params))
            session = await stack.enter_async_context(ClientSession(read_stream, write_stream))
            await session.initialize()

            namespaces = await self._list_namespaces(session)
            namespace_names = sorted(self._select_namespaces(namespaces))

            resources: List[ResourceSnapshot] = []
            for namespace in namespace_names:
                resources.extend(await self._collect_namespace(session, namespace))
            resources.sort(key=lambda item: (item.namespace, item.kind, item.name))

            snapshot = ClusterSnapshot(
                scanned_at=datetime.now(timezone.utc).isoformat(),
                cluster=self.cluster_name,
                namespaces=namespace_names,
                resources=resources,
            )
            logger.info("Collected %s resources across %s namespaces", len(resources), len(namespace_names))
            return snapshot

    def collect_sync(self) -> ClusterSnapshot:
        return asyncio.run(self.collect())

    async def _list_namespaces(self, session: ClientSession) -> List[str]:
        response = await session.call_tool("list_namespaces", {})
        payload = self._decode_response(response)
        namespaces = [entry["name"] for entry in payload.get("namespaces", []) if entry.get("name")]
        if self.namespace and self.namespace not in namespaces:
            namespaces.append(self.namespace)
        return namespaces

    def _select_namespaces(self, namespaces: List[str]) -> List[str]:
        if self.namespace:
            return [self.namespace]
        return namespaces

    async def _collect_namespace(self, session: ClientSession, namespace: str) -> List[ResourceSnapshot]:
        resources: List[ResourceSnapshot] = []
        for tool_name in (
            "list_deployments",
            "list_pods",
            "list_services",
            "list_pvcs",
            "list_configmaps",
        ):
            response = await session.call_tool(tool_name, {"namespace": namespace})
            payload = self._decode_response(response)
            for item in payload.get("items", []):
                resources.append(ResourceSnapshot.model_validate(item))
        return resources

    def _decode_response(self, response: Any) -> Dict[str, Any]:
        content = getattr(response, "content", None)
        if content:
            text_parts: List[str] = []
            for item in content:
                if getattr(item, "type", None) == "text":
                    text_parts.append(getattr(item, "text", ""))
            text = "".join(text_parts).strip()
            if text:
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    return {"items": [], "text": text}
        if isinstance(response, dict):
            return response
        if isinstance(response, list):
            return {"items": response}
        return {"items": []}
