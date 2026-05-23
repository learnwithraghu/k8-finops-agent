import requests
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def send_to_tracker(findings):
    logger.info("Sending findings to issue tracker...")
    base_url = os.getenv("ISSUE_TRACKER_URL")
    
    if not base_url:
        logger.warning("ISSUE_TRACKER_URL not configured, skipping tracker")
        return
    
    # Construct the full endpoint URL
    if not base_url.endswith("/"):
        base_url += "/"
    url = f"{base_url}create-issue"
    
    for finding in findings:
        payload = {
            "title": f"[{finding['namespace']}/{finding['pod_name']}] {finding['issue']}",
            "description": finding["recommendation"],
            "source": "simple-agent"
        }
        resp = requests.post(url, json=payload)
        if resp.status_code in [200, 201]:
            logger.info("Created issue for %s/%s", finding["namespace"], finding["pod_name"])
        else:
            logger.warning("Failed to create issue (status %d): %s", resp.status_code, resp.text)
    logger.info("Done sending to tracker")
