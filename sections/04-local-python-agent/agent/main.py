"""Main orchestrator for K8s FinOps Agent."""

import os
import sys
import logging
from pathlib import Path
from typing import Optional

import yaml
from dotenv import load_dotenv

from agent.scanner import K8sScanner
from agent.simple_checker import SimpleTagChecker


def setup_logging(log_level: str = "INFO"):
    """Setup logging configuration."""
    level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


class FinOpsAgent:
    """Main FinOps Agent orchestrator."""

    def __init__(self, config: Optional[dict] = None):
        """Initialize agent with configuration."""
        self.config = config or {}
        self.scanner = None
        self.checker = None

    def initialize(self) -> bool:
        """Initialize all components."""
        logger = logging.getLogger(__name__)

        # Initialize scanner
        kubeconfig = self.config.get('kubeconfig_path')
        excluded_namespaces = self.config.get('excluded_namespaces', [])
        self.scanner = K8sScanner(kubeconfig_path=kubeconfig, excluded_namespaces=excluded_namespaces)
        if not self.scanner.connect():
            logger.error("Failed to connect to Kubernetes")
            return False

        # Initialize tag checker
        tagging_rules = self.config.get('tagging_rules')
        self.checker = SimpleTagChecker(tagging_rules)
        logger.info("Tag checker initialized")

        return True

    def run_scan(self) -> dict:
        """Run the full scan and analysis."""
        logger = logging.getLogger(__name__)

        # Scan resources
        target_ns = self.config.get('target_namespace')
        logger.info(f"Scanning resources in namespace: {target_ns or 'all namespaces'}")
        resources = self.scanner.scan_all(target_ns)
        logger.info(f"Found {len(resources)} resources")

        # Check tags
        logger.info("Checking tagging compliance...")
        analysis = self.checker.check_all(resources)

        # Print report
        self.checker.print_report(analysis)

        return {
            'analysis': analysis,
            'total_resources': len(resources),
            'compliant_count': analysis['compliant_count'],
            'non_compliant_count': analysis['non_compliant_count']
        }


def load_config() -> dict:
    """Load configuration from environment."""
    # Load .env file if it exists
    env_path = Path('.env')
    if env_path.exists():
        load_dotenv()

    tagging_rules_path = os.getenv('TAGGING_RULES')
    excluded_namespaces = []
    if tagging_rules_path:
        try:
            rules_file = Path(tagging_rules_path).expanduser()
            if rules_file.exists():
                with open(rules_file, 'r') as f:
                    tagging_rules_data = yaml.safe_load(f) or {}
                excluded_namespaces = tagging_rules_data.get('excluded_namespaces', []) or []
        except Exception:
            excluded_namespaces = []

    return {
        'kubeconfig_path': os.getenv('KUBECONFIG_PATH'),
        'tagging_rules': tagging_rules_path,
        'log_level': os.getenv('LOG_LEVEL', 'INFO'),
        'excluded_namespaces': excluded_namespaces,
    }


def main():
    """Main entry point."""
    config = load_config()

    setup_logging(config.get('log_level', 'INFO'))
    logger = logging.getLogger(__name__)

    logger.info("Starting K8s FinOps Agent")

    agent = FinOpsAgent(config)
    if not agent.initialize():
        logger.error("Failed to initialize agent")
        sys.exit(1)

    try:
        results = agent.run_scan()
        logger.info("FinOps scan completed successfully")
        logger.info(f"Total resources: {results['total_resources']}")
        logger.info(f"Compliant: {results['compliant_count']}")
        logger.info(f"Non-compliant: {results['non_compliant_count']}")
    except Exception as e:
        logger.error(f"Scan failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()