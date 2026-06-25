"""MCP server that exposes Kubernetes read operations as tools."""

from __future__ import annotations

import json
import os
from typing import Optional

from mcp.server.fastmcp import FastMCP

from mcp_server.k8s_client import KubernetesClient

mcp = FastMCP("kubernetes-mcp-server")
_client: Optional[KubernetesClient] = None


def get_client() -> KubernetesClient:
    global _client
    if _client is None:
        kubeconfig_path = os.getenv("KUBECONFIG_PATH") or None
        excluded_namespaces = [
            ns.strip()
            for ns in os.getenv("EXCLUDED_NAMESPACES", "").split(",")
            if ns.strip()
        ] or None
        _client = KubernetesClient(
            kubeconfig_path=kubeconfig_path,
            excluded_namespaces=excluded_namespaces,
        )
    return _client


@mcp.tool()
def list_namespaces() -> str:
    """Return all non-system namespaces."""

    namespaces = [
        {"name": namespace.name, "labels": namespace.labels}
        for namespace in get_client().list_namespaces()
    ]
    return json.dumps({"namespaces": namespaces}, indent=2)


@mcp.tool()
def list_deployments(namespace: str = "") -> str:
    """Return deployments and their resource requests."""

    items = get_client().list_deployments(namespace or None)
    return json.dumps({"items": items}, indent=2)


@mcp.tool()
def list_pods(namespace: str = "") -> str:
    """Return pods with status, node assignment, and restart counts."""

    items = get_client().list_pods(namespace or None)
    return json.dumps({"items": items}, indent=2)


@mcp.tool()
def list_services(namespace: str = "") -> str:
    """Return services and their types."""

    items = get_client().list_services(namespace or None)
    return json.dumps({"items": items}, indent=2)


@mcp.tool()
def list_pvcs(namespace: str = "") -> str:
    """Return PVCs with size and mount status."""

    items = get_client().list_pvcs(namespace or None)
    return json.dumps({"items": items}, indent=2)


@mcp.tool()
def list_configmaps(namespace: str = "") -> str:
    """Return configmaps excluding common system configmaps."""

    items = get_client().list_configmaps(namespace or None)
    return json.dumps({"items": items}, indent=2)


if __name__ == "__main__":
    mcp.run()
