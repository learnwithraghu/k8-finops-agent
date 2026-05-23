import subprocess
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_k8_data():
    logger.info("Fetching Kubernetes data...")
    
    # Try metrics API first
    result = subprocess.run(
        ["kubectl", "top", "pods", "--all-namespaces"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        logger.info("Got k8 data from metrics API successfully")
        return result.stdout
    
    logger.warning("Metrics API not available, falling back to resource requests/limits...")
    
    # Fallback: get resource requests and limits from pod specs
    fallback = subprocess.run(
        ["kubectl", "get", "pods", "--all-namespaces", "-o", "json"],
        capture_output=True,
        text=True
    )
    if fallback.returncode != 0:
        logger.error("Failed to get k8 data: %s", fallback.stderr)
        return None
    
    try:
        pods = json.loads(fallback.stdout)
        lines = ["NAMESPACE\tNAME\tCPU_REQUEST\tCPU_LIMIT\tMEM_REQUEST\tMEM_LIMIT"]
        for pod in pods.get("items", []):
            ns = pod["metadata"]["namespace"]
            name = pod["metadata"]["name"]
            for container in pod["spec"].get("containers", []):
                resources = container.get("resources", {})
                req = resources.get("requests", {})
                lim = resources.get("limits", {})
                lines.append(
                    f"{ns}\t{name}\t{req.get('cpu', 'N/A')}\t{lim.get('cpu', 'N/A')}\t{req.get('memory', 'N/A')}\t{lim.get('memory', 'N/A')}"
                )
        logger.info("Got k8 data from pod specs successfully")
        return "\n".join(lines)
    except Exception as e:
        logger.error("Failed to parse pod data: %s", e)
        return None
