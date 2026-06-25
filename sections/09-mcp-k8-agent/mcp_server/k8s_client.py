"""Thin Kubernetes client wrapper used by the MCP server."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set

from kubernetes import client, config
from kubernetes.client import ApiException
from kubernetes.config.config_exception import ConfigException

DEFAULT_EXCLUDED_NAMESPACES = {
    "kube-system",
    "kube-public",
    "kube-node-lease",
    "local-path-storage",
}


@dataclass(frozen=True)
class NamespaceRef:
    name: str
    labels: Dict[str, str]


class KubernetesClient:
    """Small convenience wrapper around the Kubernetes Python client."""

    def __init__(
        self,
        kubeconfig_path: Optional[str] = None,
        excluded_namespaces: Optional[List[str]] = None,
    ) -> None:
        self.kubeconfig_path = kubeconfig_path
        self.excluded_namespaces: Set[str] = set(excluded_namespaces or DEFAULT_EXCLUDED_NAMESPACES)
        self._connected = False
        self.v1: Optional[client.CoreV1Api] = None
        self.apps_v1: Optional[client.AppsV1Api] = None

    def connect(self) -> None:
        """Load kubeconfig or fall back to in-cluster config."""

        if self._connected:
            return

        if self.kubeconfig_path:
            config.load_kube_config(config_file=str(Path(self.kubeconfig_path).expanduser()))
        else:
            try:
                config.load_kube_config()
            except ConfigException:
                config.load_incluster_config()

        self.v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
        self._connected = True

    def list_namespaces(self) -> List[NamespaceRef]:
        self._ensure_connected()
        assert self.v1 is not None

        try:
            response = self.v1.list_namespace()
        except ApiException:
            return []

        namespaces: List[NamespaceRef] = []
        for item in response.items:
            name = item.metadata.name if item.metadata else ""
            if self._is_excluded_namespace(name):
                continue
            namespaces.append(
                NamespaceRef(
                    name=name,
                    labels=dict(item.metadata.labels or {}),
                )
            )
        return namespaces

    def list_deployments(self, namespace: Optional[str] = None) -> List[Dict[str, object]]:
        self._ensure_connected()
        assert self.apps_v1 is not None

        try:
            response = (
                self.apps_v1.list_namespaced_deployment(namespace)
                if namespace
                else self.apps_v1.list_deployment_for_all_namespaces()
            )
        except ApiException:
            return []

        deployments: List[Dict[str, object]] = []
        for item in response.items:
            ns = item.metadata.namespace if item.metadata else ""
            if self._is_excluded_namespace(ns):
                continue
            cpu_request_m, memory_request_mi = self._sum_container_requests(
                getattr(item.spec.template.spec, "containers", []) if item.spec and item.spec.template and item.spec.template.spec else []
            )
            pvc_names = self._pvc_names_from_volumes(
                getattr(item.spec.template.spec, "volumes", []) if item.spec and item.spec.template and item.spec.template.spec else []
            )
            deployments.append(
                self._base_resource(
                    kind="Deployment",
                    namespace=ns,
                    name=item.metadata.name,
                    labels=dict(item.metadata.labels or {}),
                    annotations=dict(item.metadata.annotations or {}),
                    owners=self._owner_refs(item.metadata.owner_references),
                    replicas=item.spec.replicas if item.spec and item.spec.replicas is not None else 1,
                    cpu_request_m=cpu_request_m,
                    memory_request_mi=memory_request_mi,
                    pvc_names=pvc_names,
                )
            )
        return deployments

    def list_pods(self, namespace: Optional[str] = None) -> List[Dict[str, object]]:
        self._ensure_connected()
        assert self.v1 is not None

        try:
            response = (
                self.v1.list_namespaced_pod(namespace)
                if namespace
                else self.v1.list_pod_for_all_namespaces()
            )
        except ApiException:
            return []

        pods: List[Dict[str, object]] = []
        for item in response.items:
            ns = item.metadata.namespace if item.metadata else ""
            if self._is_excluded_namespace(ns):
                continue

            cpu_request_m, memory_request_mi = self._sum_container_requests(item.spec.containers if item.spec and item.spec.containers else [])
            restart_count = self._restart_count(item.status.container_statuses if item.status else None)
            pods.append(
                self._base_resource(
                    kind="Pod",
                    namespace=ns,
                    name=item.metadata.name,
                    labels=dict(item.metadata.labels or {}),
                    annotations=dict(item.metadata.annotations or {}),
                    owners=self._owner_refs(item.metadata.owner_references),
                    cpu_request_m=cpu_request_m,
                    memory_request_mi=memory_request_mi,
                    phase=getattr(item.status, "phase", None),
                    node_name=getattr(item.spec, "node_name", None),
                    restart_count=restart_count,
                )
            )
        return pods

    def list_services(self, namespace: Optional[str] = None) -> List[Dict[str, object]]:
        self._ensure_connected()
        assert self.v1 is not None

        try:
            response = (
                self.v1.list_namespaced_service(namespace)
                if namespace
                else self.v1.list_service_for_all_namespaces()
            )
        except ApiException:
            return []

        services: List[Dict[str, object]] = []
        for item in response.items:
            ns = item.metadata.namespace if item.metadata else ""
            if self._is_excluded_namespace(ns):
                continue
            if item.metadata and item.metadata.name == "kubernetes":
                continue

            services.append(
                self._base_resource(
                    kind="Service",
                    namespace=ns,
                    name=item.metadata.name,
                    labels=dict(item.metadata.labels or {}),
                    annotations=dict(item.metadata.annotations or {}),
                    owners=self._owner_refs(item.metadata.owner_references),
                    service_type=getattr(item.spec, "type", None),
                    selector=dict(getattr(item.spec, "selector", {}) or {}),
                )
            )
        return services

    def list_pvcs(self, namespace: Optional[str] = None) -> List[Dict[str, object]]:
        self._ensure_connected()
        assert self.v1 is not None

        try:
            response = (
                self.v1.list_namespaced_persistent_volume_claim(namespace)
                if namespace
                else self.v1.list_persistent_volume_claim_for_all_namespaces()
            )
        except ApiException:
            return []

        mounted_map = self._mounted_pvcs(namespace)
        pvcs: List[Dict[str, object]] = []
        for item in response.items:
            ns = item.metadata.namespace if item.metadata else ""
            if self._is_excluded_namespace(ns):
                continue

            size_gi = self._parse_storage(
                getattr(getattr(item.spec, "resources", None), "requests", {}).get("storage", "0")
                if item.spec else "0"
            )
            mounted_by = sorted(mounted_map.get((ns, item.metadata.name), []))
            pvcs.append(
                self._base_resource(
                    kind="PersistentVolumeClaim",
                    namespace=ns,
                    name=item.metadata.name,
                    labels=dict(item.metadata.labels or {}),
                    annotations=dict(item.metadata.annotations or {}),
                    owners=self._owner_refs(item.metadata.owner_references),
                    pvc_size_gi=size_gi,
                    is_bound=getattr(item.status, "phase", None) == "Bound",
                    is_mounted=bool(mounted_by),
                    mounted_by=mounted_by,
                )
            )
        return pvcs

    def list_configmaps(self, namespace: Optional[str] = None) -> List[Dict[str, object]]:
        self._ensure_connected()
        assert self.v1 is not None

        try:
            response = (
                self.v1.list_namespaced_config_map(namespace)
                if namespace
                else self.v1.list_config_map_for_all_namespaces()
            )
        except ApiException:
            return []

        configmaps: List[Dict[str, object]] = []
        for item in response.items:
            ns = item.metadata.namespace if item.metadata else ""
            if self._is_excluded_namespace(ns):
                continue
            if item.metadata and item.metadata.name == "kube-root-ca.crt":
                continue

            configmaps.append(
                self._base_resource(
                    kind="ConfigMap",
                    namespace=ns,
                    name=item.metadata.name,
                    labels=dict(item.metadata.labels or {}),
                    annotations=dict(item.metadata.annotations or {}),
                    owners=self._owner_refs(item.metadata.owner_references),
                    configmap_keys=sorted(list((item.data or {}).keys())),
                )
            )
        return configmaps

    def _mounted_pvcs(self, namespace: Optional[str] = None) -> Dict[tuple[str, str], List[str]]:
        self._ensure_connected()
        assert self.v1 is not None

        mounted: Dict[tuple[str, str], List[str]] = {}
        try:
            response = (
                self.v1.list_namespaced_pod(namespace)
                if namespace
                else self.v1.list_pod_for_all_namespaces()
            )
        except ApiException:
            return mounted

        for pod in response.items:
            ns = pod.metadata.namespace if pod.metadata else ""
            if self._is_excluded_namespace(ns):
                continue
            for volume in getattr(pod.spec, "volumes", []) or []:
                pvc = getattr(volume, "persistent_volume_claim", None)
                if pvc and pvc.claim_name:
                    mounted.setdefault((ns, pvc.claim_name), []).append(pod.metadata.name)
        return mounted

    def _base_resource(self, **kwargs: object) -> Dict[str, object]:
        payload: Dict[str, object] = {
            "labels": {},
            "annotations": {},
            "owners": [],
            "cpu_request_m": 0,
            "memory_request_mi": 0,
            "pvc_names": [],
            "configmap_keys": [],
            "mounted_by": [],
            "selector": {},
        }
        payload.update(kwargs)
        return payload

    def _owner_refs(self, owner_references: Optional[List[object]]) -> List[str]:
        owners: List[str] = []
        for owner in owner_references or []:
            kind = getattr(owner, "kind", None)
            name = getattr(owner, "name", None)
            if kind and name:
                owners.append(f"{kind}/{name}")
        return owners

    def _sum_container_requests(self, containers: List[object]) -> tuple[int, int]:
        cpu_request_m = 0
        memory_request_mi = 0
        for container in containers or []:
            resources = getattr(container, "resources", None)
            requests = getattr(resources, "requests", None) if resources else None
            if requests:
                cpu_request_m += self._parse_cpu(requests.get("cpu", "0"))
                memory_request_mi += self._parse_memory(requests.get("memory", "0"))
        return cpu_request_m, memory_request_mi

    def _pvc_names_from_volumes(self, volumes: List[object]) -> List[str]:
        pvc_names: List[str] = []
        for volume in volumes or []:
            pvc = getattr(volume, "persistent_volume_claim", None)
            if pvc and pvc.claim_name:
                pvc_names.append(pvc.claim_name)
        return sorted(pvc_names)

    def _restart_count(self, container_statuses: Optional[List[object]]) -> int:
        total = 0
        for status in container_statuses or []:
            total += int(getattr(status, "restart_count", 0) or 0)
        return total

    def _is_excluded_namespace(self, namespace: Optional[str]) -> bool:
        return bool(namespace and namespace in self.excluded_namespaces)

    def _ensure_connected(self) -> None:
        if not self._connected:
            self.connect()

    @staticmethod
    def _parse_cpu(cpu_str: str) -> int:
        if not cpu_str:
            return 0
        if cpu_str.endswith("m"):
            return int(float(cpu_str[:-1]))
        return int(float(cpu_str) * 1000)

    @staticmethod
    def _parse_memory(mem_str: str) -> int:
        if not mem_str:
            return 0
        if mem_str.endswith("Gi"):
            return int(float(mem_str[:-2]) * 1024)
        if mem_str.endswith("Mi"):
            return int(float(mem_str[:-2]))
        if mem_str.endswith("Ki"):
            return int(float(mem_str[:-2]) / 1024)
        return int(float(mem_str) / (1024 * 1024))

    @staticmethod
    def _parse_storage(storage_str: str) -> float:
        if not storage_str:
            return 0.0
        if storage_str.endswith("Gi"):
            return float(storage_str[:-2])
        if storage_str.endswith("Mi"):
            return float(storage_str[:-2]) / 1024
        if storage_str.endswith("Ti"):
            return float(storage_str[:-2]) * 1024
        return float(storage_str)
