import json
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Add section to Python path so we can import modules
sys.path.insert(0, str(Path(__file__).parent))

from k8_data import get_k8_data
from bedrock_client import analyze_with_bedrock
from issue_tracker import send_to_tracker

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_env():
    """Load environment variables from the repo root .env file."""
    # Look for .env in current working directory (root of repo)
    # This supports running: PYTHONPATH=sections/09-simple-agent-example python -m main
    env_path = Path('.env')
    if env_path.exists():
        load_dotenv(dotenv_path=str(env_path), override=True)
        logger.info("Loaded .env from %s", env_path.resolve())
    else:
        # Fallback: try parent directories
        for parent in Path.cwd().parents:
            env_file = parent / ".env"
            if env_file.exists():
                load_dotenv(dotenv_path=str(env_file), override=True)
                logger.info("Loaded .env from %s", env_file.resolve())
                return
        logger.warning("Root .env not found, using system environment")

def main():
    logger.info("Starting simple agent...")
    load_env()

    data = get_k8_data()
    if not data:
        logger.error("No k8 data. Exiting.")
        return

    raw_response = analyze_with_bedrock(data)
    
    if not raw_response:
        logger.error("Bedrock returned empty response")
        findings = []
    else:
        # Try to extract JSON array from response
        try:
            logger.debug(f"Raw response: {raw_response[:500]}")
            # Find JSON array in the response text
            start = raw_response.find("[")
            end = raw_response.rfind("]") + 1
            
            if start < 0 or end <= start:
                logger.error("Response does not contain a JSON array")
                logger.error(f"Full response: {raw_response}")
                findings = []
            else:
                json_str = raw_response[start:end]
                findings = json.loads(json_str)
                logger.info(f"Parsed {len(findings)} findings from Bedrock")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from Bedrock response: {e}")
            logger.error(f"Response text: {raw_response}")
            findings = []
        except Exception as e:
            logger.error(f"Unexpected error parsing Bedrock response: {e}")
            findings = []

    if findings:
        send_to_tracker(findings)
    else:
        logger.info("No findings to report.")

    logger.info("Agent run complete.")

if __name__ == "__main__":
    main()
