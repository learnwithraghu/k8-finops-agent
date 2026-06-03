"""Simple Kubernetes resource scanner for FinOps agent."""

from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

logger = logging.getLogger(__name__)


class K8sScanner:
    """Scans Kubernetes cluster for resources and their tags."""

    def __init__(self, kubeconfig_path: Optional[str] = None, excluded_namespaces: Optional[List[str]] = None):
        """Initialize scanner with optional kubeconfig path."""
        self.kubeconfig_path = kubeconfig_path
        self.excluded_namespaces = set(excluded_namespaces or [])
        self.v1 = None
        self.apps_v1 = None
        self._connected = False

    def connect(self) -> bool:
        """Connect to Kubernetes cluster."""
        try:
            if self.kubeconfig_path:
                kubeconfig_file = str(Path(self.kubeconfig_path).expanduser())
                config.load_kube_config(config_file=kubeconfig_file)
            else:
                config.load_kube_config()

            self.v1 = client.CoreV1Api()
            self.apps_v1 = client.AppsV1Api()
            self._connected = True
            logger.info("Connected to Kubernetes cluster")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Kubernetes: {e}")
            return False

    def get_all_namespaces(self) -> List[str]:
        """Get list of all namespaces in the cluster."""
        if not self._connected:
            raise RuntimeError("Scanner not connected to cluster")

        try:
            ns_list = self.v1.list_namespace()
            return [ns.metadata.name for ns in ns_list.items]
        except ApiException as e:
            logger.error(f"Failed to list namespaces: {e}")
            return []

    def scan_deployments(self, namespace: Optional[str] = None) -> List[Dict[str, Any]]:
        """Scan deployments in the cluster."""
        if not self._connected:
            raise RuntimeError("Scanner not connected to cluster")

        if namespace and self._is_excluded_namespace(namespace):
            logger.info(f"Skipping excluded namespace: {namespace}")
            return []

        resources = []
        try:
            if namespace:
                deps = self.apps_v1.list_namespaced_deployment(namespace)
            else:
                deps = self.apps_v1.list_deployment_for_all_namespaces()

            for dep in deps.items:
                if self._is_excluded_namespace(dep.metadata.namespace):
                    continue

                resource = {
                    'name': dep.metadata.name,
                    'namespace': dep.metadata.namespace,
                    'kind': 'Deployment',
                    'labels': dep.metadata.labels or {},
                    'annotations': dep.metadata.annotations or {},
                    'replicas': dep.spec.replicas or 1
                }
                resources.append(resource)

        except ApiException as e:
            logger.error(f"Failed to scan deployments: {e}")

        return resources

    def scan_services(self, namespace: Optional[str] = None) -> List[Dict[str, Any]]:
        """Scan services in the cluster."""
        if not self._connected:
            raise RuntimeError("Scanner not connected to cluster")

        if namespace and self._is_excluded_namespace(namespace):
            logger.info(f"Skipping excluded namespace: {namespace}")
            return []

        resources = []
        try:
            if namespace:
                svcs = self.v1.list_namespaced_service(namespace)
            else:
                svcs = self.v1.list_service_for_all_namespaces()

            for svc in svcs.items:
                if self._is_excluded_namespace(svc.metadata.namespace):
                    continue
                if svc.metadata.name == 'kubernetes':
                    continue

                resource = {
                    'name': svc.metadata.name,
                    'namespace': svc.metadata.namespace,
                    'kind': 'Service',
                    'labels': svc.metadata.labels or {},
                    'annotations': svc.metadata.annotations or {}
                }
                resources.append(resource)

        except ApiException as e:
            logger.error(f"Failed to scan services: {e}")

        return resources

    def scan_configmaps(self, namespace: Optional[str] = None) -> List[Dict[str, Any]]:
        """Scan configmaps in the cluster."""
        if not self._connected:
            raise RuntimeError("Scanner not connected to cluster")

        if namespace and self._is_excluded_namespace(namespace):
            logger.info(f"Skipping excluded namespace: {namespace}")
            return []

        resources = []
        try:
            if namespace:
                cms = self.v1.list_namespaced_config_map(namespace)
            else:
                cms = self.v1.list_config_map_for_all_namespaces()

            for cm in cms.items:
                if self._is_excluded_namespace(cm.metadata.namespace):
                    continue
                if cm.metadata.name == 'kube-root-ca.crt':
                    continue

                resource = {
                    'name': cm.metadata.name,
                    'namespace': cm.metadata.namespace,
                    'kind': 'ConfigMap',
                    'labels': cm.metadata.labels or {},
                    'annotations': cm.metadata.annotations or {}
                }
                resources.append(resource)

        except ApiException as e:
            logger.error(f"Failed to scan configmaps: {e}")

        return resources

    def scan_pvcs(self, namespace: Optional[str] = None) -> List[Dict[str, Any]]:
        """Scan PVCs and identify orphaned ones."""
        if not self._connected:
            raise RuntimeError("Scanner not connected to cluster")

        if namespace and self._is_excluded_namespace(namespace):
            logger.info(f"Skipping excluded namespace: {namespace}")
            return []

        resources = []
        try:
            if namespace:
                pvcs = self.v1.list_namespaced_persistent_volume_claim(namespace)
            else:
                pvcs = self.v1.list_persistent_volume_claim_for_all_namespaces()

            mounted_pvcs = self._get_mounted_pvcs(namespace)

            for pvc in pvcs.items:
                if self._is_excluded_namespace(pvc.metadata.namespace):
                    continue

                size_gb = self._parse_storage(pvc.spec.resources.requests.get('storage', '0'))
                is_orphaned = (pvc.metadata.namespace, pvc.metadata.name) not in mounted_pvcs

                resource = {
                    'name': pvc.metadata.name,
                    'namespace': pvc.metadata.namespace,
                    'kind': 'PersistentVolumeClaim',
                    'labels': pvc.metadata.labels or {},
                    'annotations': pvc.metadata.annotations or {},
                    'size_gb': size_gb,
                    'is_orphaned': is_orphaned
                }
                resources.append(resource)

        except ApiException as e:
            logger.error(f"Failed to scan PVCs: {e}")

        return resources

    def _get_mounted_pvcs(self, namespace: Optional[str] = None) -> set:
        """Get set of (namespace, pvc_name) tuples that are mounted by pods."""
        mounted = set()
        try:
            if namespace:
                pods = self.v1.list_namespaced_pod(namespace)
            else:
                pods = self.v1.list_pod_for_all_namespaces()

            for pod in pods.items:
                if self._is_excluded_namespace(pod.metadata.namespace):
                    continue
                if pod.spec.volumes:
                    for vol in pod.spec.volumes:
                        if vol.persistent_volume_claim:
                            mounted.add((
                                pod.metadata.namespace,
                                vol.persistent_volume_claim.claim_name
                            ))
        except ApiException:
            pass
        return mounted

    def scan_all(self, namespace: Optional[str] = None) -> List[Dict[str, Any]]:
        """Scan all resource types and return combined list."""
        resources = []
        resources.extend(self.scan_deployments(namespace))
        resources.extend(self.scan_services(namespace))
        resources.extend(self.scan_configmaps(namespace))
        resources.extend(self.scan_pvcs(namespace))
        logger.info(f"Scanned {len(resources)} total resources")
        return resources

    def _is_excluded_namespace(self, namespace: Optional[str]) -> bool:
        """Return True when a namespace should be skipped."""
        return bool(namespace and namespace in self.excluded_namespaces)

    @staticmethod
    def _parse_storage(storage_str: str) -> float:
        """Parse storage string to GB."""
        if not storage_str:
            return 0.0
        if storage_str.endswith('Gi'):
            return float(storage_str[:-2])
        if storage_str.endswith('Mi'):
            return float(storage_str[:-2]) / 1024
        if storage_str.endswith('Ti'):
            return float(storage_str[:-2]) * 1024
        return float(storage_str)