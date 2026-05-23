import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def send_to_tracker(findings, config):
    logger.info("Sending findings to issue tracker...")
    url = config.get("tracker_url", "http://localhost:8080/issues")
    for finding in findings:
        payload = {
            "title": f"[{finding['namespace']}/{finding['pod_name']}] {finding['issue']}",
            "description": finding["recommendation"],
            "source": "simple-agent"
        }
        resp = requests.post(url, json=payload)
        if resp.status_code == 201:
            logger.info("Created issue for %s/%s", finding["namespace"], finding["pod_name"])
        else:
            logger.warning("Failed to create issue: %s", resp.text)
    logger.info("Done sending to tracker")
