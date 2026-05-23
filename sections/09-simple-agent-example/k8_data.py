import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_k8_data():
    logger.info("Fetching Kubernetes data...")
    result = subprocess.run(
        ["kubectl", "top", "pods", "--all-namespaces"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        logger.error("Failed to get k8 data: %s", result.stderr)
        return None
    logger.info("Got k8 data successfully")
    return result.stdout
