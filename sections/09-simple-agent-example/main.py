import json
import logging
import os

import yaml
from dotenv import load_dotenv

from k8_data import get_k8_data
from bedrock_client import analyze_with_bedrock
from issue_tracker import send_to_tracker

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config(path="config.yaml"):
    logger.info("Loading config from %s and .env", path)
    load_dotenv()
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    # Override with .env if present
    config["region"] = os.getenv("AWS_REGION", config.get("region", "us-east-1"))
    config["model_id"] = os.getenv("BEDROCK_MODEL_ID", config.get("model_id"))
    config["tracker_url"] = os.getenv("TRACKER_URL", config.get("tracker_url", "http://localhost:8080/issues"))
    return config

def main():
    logger.info("Starting simple agent...")

    config = load_config()
    data = get_k8_data()
    if not data:
        logger.error("No k8 data. Exiting.")
        return

    raw_response = analyze_with_bedrock(data, config)
    # Try to extract JSON array from response
    try:
        # Find JSON array in the response text
        start = raw_response.find("[")
        end = raw_response.rfind("]") + 1
        findings = json.loads(raw_response[start:end])
    except Exception as e:
        logger.error("Failed to parse Bedrock response: %s", e)
        findings = []

    if findings:
        send_to_tracker(findings, config)
    else:
        logger.info("No findings to report.")

    logger.info("Agent run complete.")

if __name__ == "__main__":
    main()
