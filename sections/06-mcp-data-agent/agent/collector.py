"""Collect raw Kubernetes data through MCP tools."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import shlex
from contextlib import AsyncExitStack
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from mcp import ClientSession
except ImportError:  # pragma: no cover - compatibility with older SDK layouts
    from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

logger = logging.getLogger(__name__)

TOOLS = ("list_deployments", "list_pods", "list_services", "list_pvcs", "list_configmaps")


def _default_kubeconfig_file() -> str:
    return os.getenv("KUBECONFIG_FILE") or os.getenv("KUBECONFIG") or str(Path.home() / ".kube" / "config")


def _server_command_and_args() -> tuple[str, List[str]]:
    command = os.getenv("MCP_SERVER_COMMAND", "docker")
    explicit_args = os.getenv("MCP_SERVER_ARGS")
    if explicit_args:
        return command, shlex.split(explicit_args)

    kubeconfig_file = _default_kubeconfig_file()
    args = [
        "run",
        "--rm",
        "-i",
        "--user",
        "0:0",
        "-v",
        f"{kubeconfig_file}:/kubeconfig:ro",
        "-e",
        "KUBECONFIG=/kubeconfig",
        "mcp/kubernetes:latest",
    ]
    return command, args


async def collect_snapshot(cluster_name: Optional[str] = None) -> Dict[str, Any]:
    command, args = _server_command_and_args()
    server_params = StdioServerParameters(
        command=command,
        args=args,
        env=os.environ.copy(),
    )

    async with AsyncExitStack() as stack:
        read_stream, write_stream = await stack.enter_async_context(stdio_client(server_params))
        session = await stack.enter_async_context(ClientSession(read_stream, write_stream))
        await session.initialize()

        payload = _decode(await session.call_tool("list_namespaces", {}))
        namespaces = [item["name"] for item in payload.get("namespaces", []) if item.get("name")]
        resources: List[Dict[str, Any]] = []
        for ns in namespaces:
            for tool_name in TOOLS:
                response = await session.call_tool(tool_name, {"namespace": ns})
                resources.extend(_decode(response).get("items", []))

        resources.sort(key=lambda item: (item.get("namespace", ""), item.get("kind", ""), item.get("name", "")))
        return {"scanned_at": datetime.now(timezone.utc).isoformat(), "cluster": cluster_name or os.getenv("CLUSTER_NAME", "kind"), "namespaces": namespaces, "resources": resources}


def collect_snapshot_sync(cluster_name: Optional[str] = None) -> Dict[str, Any]:
    return asyncio.run(collect_snapshot(cluster_name))


def _decode(response: Any) -> Dict[str, Any]:
    content = getattr(response, "content", None)
    if content:
        text = "".join(getattr(item, "text", "") for item in content if getattr(item, "type", None) == "text").strip()
        if text:
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return {"items": []}
    if isinstance(response, dict):
        return response
    if isinstance(response, list):
        return {"items": response}
    return {"items": []}
