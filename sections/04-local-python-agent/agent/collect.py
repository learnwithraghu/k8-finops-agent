"""Kubernetes metadata collector for FinOps agent.

This script does one thing: read raw Kubernetes metadata and dump it as JSON.
It does NOT decide compliance, calculate cost, or draft issues. Those decisions
are delegated to the LLM agent in Section 05.
"""

import argparse
import json
import logging
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from dotenv import load_dotenv
from kubernetes import client, config

logger = logging.getLogger(__name__)


@dataclass
class K8sResource:
    """Minimal representation of a Kubernetes resource for downstream analysis."""
    name: str
    namespace: str
    kind: str
    labels: Dict[str, str] = field(default_factory=dict)
    annotations: Dict[str, str] = field(default_factory=dict)
    cpu_request: int = 0  # millicores
    memory_request: int = 0  # Mi
    replicas: int = 1
    pvc_names: List[str] = field(default_factory=list)
    pvc_size_gb: float = 0.0
    is_orphaned: bool = False


def load_kubernetes_client(kubeconfig_path: Optional[str] = None):
    """Return a (CoreV1Api, AppsV1Api) tuple configured from kubeconfig."""
    if kubeconfig_path:
        config.load_kube_config(config_file=str(Path(kubeconfig_path).expanduser()))
    else:
        config.load_kube_config()
    return client.CoreV1Api(), client.AppsV1Api()


def is_excluded_namespace(namespace: Optional[str], excluded: set) -> bool:
    return bool(namespace and namespace in excluded)


def parse_cpu(cpu_str: Optional[str]) -> int:
    if not cpu_str:
        return 0
    if str(cpu_str).endswith("m"):
        return int(str(cpu_str)[:-1])
    return int(float(cpu_str) * 1000)


def parse_memory(mem_str: Optional[str]) -> int:
    if not mem_str:
        return 0
    mem = str(mem_str)
    if mem.endswith("Gi"):
        return int(float(mem[:-2]) * 1024)
    if mem.endswith("Mi"):
        return int(mem[:-2])
    if mem.endswith("Ki"):
        return int(float(mem[:-2]) / 1024)
    return int(float(mem) / (1024 * 1024))


def parse_storage(storage_str: Optional[str]) -> float:
    if not storage_str:
        return 0.0
    storage = str(storage_str)
    if storage.endswith("Gi"):
        return float(storage[:-2])
    if storage.endswith("Mi"):
        return float(storage[:-2]) / 1024
    if storage.endswith("Ti"):
        return float(storage[:-2]) * 1024
    return float(storage)


def get_mounted_pvcs(v1: client.CoreV1Api, namespace: Optional[str], excluded: set) -> set:
    mounted = set()
    pods = v1.list_namespaced_pod(namespace) if namespace else v1.list_pod_for_all_namespaces()
    for pod in pods.items:
        if is_excluded_namespace(pod.metadata.namespace, excluded):
            continue
        for vol in pod.spec.volumes or []:
            if vol.persistent_volume_claim:
                mounted.add((pod.metadata.namespace, vol.persistent_volume_claim.claim_name))
    return mounted


def collect_deployments(apps_v1: client.AppsV1Api, namespace: Optional[str], excluded: set) -> List[K8sResource]:
    resources = []
    deps = apps_v1.list_namespaced_deployment(namespace) if namespace else apps_v1.list_deployment_for_all_namespaces()
    for dep in deps.items:
        if is_excluded_namespace(dep.metadata.namespace, excluded):
            continue

        cpu_request = 0
        memory_request = 0
        for container in dep.spec.template.spec.containers or []:
            requests = (container.resources and container.resources.requests) or {}
            cpu_request += parse_cpu(requests.get("cpu"))
            memory_request += parse_memory(requests.get("memory"))

        pvc_names = [
            vol.persistent_volume_claim.claim_name
            for vol in dep.spec.template.spec.volumes or []
            if vol.persistent_volume_claim
        ]

        resources.append(K8sResource(
            name=dep.metadata.name,
            namespace=dep.metadata.namespace,
            kind="Deployment",
            labels=dep.metadata.labels or {},
            annotations=dep.metadata.annotations or {},
            cpu_request=cpu_request,
            memory_request=memory_request,
            replicas=dep.spec.replicas or 1,
            pvc_names=pvc_names,
        ))
    return resources


def collect_services(v1: client.CoreV1Api, namespace: Optional[str], excluded: set) -> List[K8sResource]:
    resources = []
    svcs = v1.list_namespaced_service(namespace) if namespace else v1.list_service_for_all_namespaces()
    for svc in svcs.items:
        if is_excluded_namespace(svc.metadata.namespace, excluded):
            continue
        if svc.metadata.name == "kubernetes":
            continue
        resources.append(K8sResource(
            name=svc.metadata.name,
            namespace=svc.metadata.namespace,
            kind="Service",
            labels=svc.metadata.labels or {},
            annotations=svc.metadata.annotations or {},
        ))
    return resources


def collect_configmaps(v1: client.CoreV1Api, namespace: Optional[str], excluded: set) -> List[K8sResource]:
    resources = []
    cms = v1.list_namespaced_config_map(namespace) if namespace else v1.list_config_map_for_all_namespaces()
    for cm in cms.items:
        if is_excluded_namespace(cm.metadata.namespace, excluded):
            continue
        if cm.metadata.name == "kube-root-ca.crt":
            continue
        resources.append(K8sResource(
            name=cm.metadata.name,
            namespace=cm.metadata.namespace,
            kind="ConfigMap",
            labels=cm.metadata.labels or {},
            annotations=cm.metadata.annotations or {},
        ))
    return resources


def collect_pvcs(v1: client.CoreV1Api, namespace: Optional[str], excluded: set) -> List[K8sResource]:
    resources = []
    pvcs = v1.list_namespaced_persistent_volume_claim(namespace) if namespace else v1.list_persistent_volume_claim_for_all_namespaces()
    mounted_pvcs = get_mounted_pvcs(v1, namespace, excluded)
    for pvc in pvcs.items:
        if is_excluded_namespace(pvc.metadata.namespace, excluded):
            continue
        size_gb = parse_storage(pvc.spec.resources.requests.get("storage", "0"))
        is_orphaned = (pvc.metadata.namespace, pvc.metadata.name) not in mounted_pvcs
        resources.append(K8sResource(
            name=pvc.metadata.name,
            namespace=pvc.metadata.namespace,
            kind="PersistentVolumeClaim",
            labels=pvc.metadata.labels or {},
            annotations=pvc.metadata.annotations or {},
            pvc_size_gb=size_gb,
            is_orphaned=is_orphaned,
        ))
    return resources


def collect_all(v1: client.CoreV1Api, apps_v1: client.AppsV1Api, namespace: Optional[str], excluded: set) -> List[K8sResource]:
    resources = []
    resources.extend(collect_deployments(apps_v1, namespace, excluded))
    resources.extend(collect_services(v1, namespace, excluded))
    resources.extend(collect_configmaps(v1, namespace, excluded))
    resources.extend(collect_pvcs(v1, namespace, excluded))
    return resources


def load_excluded_namespaces(rules_path: Path) -> set:
    try:
        tagging_rules = yaml.safe_load(rules_path.read_text()) or {}
        return set(tagging_rules.get("excluded_namespaces", []))
    except Exception as e:
        logger.warning(f"Could not load tagging rules, using no exclusions: {e}")
        return set()


def main():
    parser = argparse.ArgumentParser(description="Collect Kubernetes metadata as JSON")
    parser.add_argument("--namespace", help="Limit collection to a single namespace")
    parser.add_argument("--output", "-o", default="k8s_metadata.json", help="Output JSON file")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    if Path(".env").exists():
        load_dotenv()

    tagging_rules_path = Path(__file__).parent.parent / "config" / "tagging-rules.yaml"
    excluded_namespaces = load_excluded_namespaces(tagging_rules_path)

    v1, apps_v1 = load_kubernetes_client(os.getenv("KUBECONFIG_PATH"))

    logger.info(f"Collecting resources in namespace: {args.namespace or 'all namespaces'}")
    resources = collect_all(v1, apps_v1, args.namespace, excluded_namespaces)
    logger.info(f"Collected {len(resources)} resources")

    payload = {
        "metadata": {
            "namespace": args.namespace,
            "resource_count": len(resources),
            "excluded_namespaces": sorted(excluded_namespaces),
        },
        "resources": [asdict(r) for r in resources],
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(payload, indent=2))
    logger.info(f"Wrote metadata to {output_path}")

    print("\n" + "=" * 60)
    print("KUBERNETES METADATA COLLECTION COMPLETE")
    print("=" * 60)
    print(f"Resources collected: {len(resources)}")
    print(f"Output file: {output_path}")
    print("\nThis is raw cluster metadata. In Section 05, the LLM will decide")
    print("which resources are compliant and what actions to take.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
