"""Main orchestrator for K8s FinOps Agent."""

import os
import sys
import logging
import argparse
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from agent.scanner import K8sScanner
from agent.cost_calculator import CostCalculator
from agent.untracked_money import UntrackedMoneyDetector
from agent.analyzer import BedrockAnalyzer, MockAnalyzer
from agent.github_client import GitHubIssueClient, MockGitHubClient

# Configure logging
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
        self.calculator = None
        self.detector = None
        self.analyzer = None
        self.github = None

    def initialize(self) -> bool:
        """Initialize all components."""
        logger = logging.getLogger(__name__)

        # Initialize scanner
        kubeconfig = self.config.get('kubeconfig_path')
        self.scanner = K8sScanner(kubeconfig_path=kubeconfig)
        if not self.scanner.connect():
            logger.error("Failed to connect to Kubernetes")
            return False

        # Initialize cost calculator
        pricing_config = self.config.get('pricing_config')
        self.calculator = CostCalculator(pricing_config)

        # Initialize untracked money detector
        tagging_rules = self.config.get('tagging_rules')
        self.detector = UntrackedMoneyDetector(self.calculator, tagging_rules)

        # Initialize analyzer (Bedrock or Mock)
        use_mock = self.config.get('use_mock', False)
        if use_mock:
            self.analyzer = MockAnalyzer()
            logger.info("Using mock analyzer")
        else:
            model_id = self.config.get('bedrock_model_id')
            region = self.config.get('aws_region', 'us-east-1')
            self.analyzer = BedrockAnalyzer(model_id, region)

        if not self.analyzer.connect():
            logger.warning("Failed to connect to Bedrock, falling back to mock analyzer")
            self.analyzer = MockAnalyzer()

        # Initialize GitHub client (real or mock)
        use_mock_github = self.config.get('use_mock_github', False)
        if use_mock_github:
            self.github = MockGitHubClient()
            logger.info("Using mock GitHub client")
        else:
            token = self.config.get('github_token')
            repo = self.config.get('github_repo')
            self.github = GitHubIssueClient(token, repo)

        if not self.github.connect():
            logger.warning("Failed to connect to GitHub, falling back to mock client")
            self.github = MockGitHubClient()

        return True

    def run_scan(self) -> dict:
        """Run the full scan and analysis."""
        logger = logging.getLogger(__name__)

        # Scan resources
        target_ns = self.config.get('target_namespace')
        logger.info(f"Scanning resources in namespace: {target_ns or 'all'}")
        resources = self.scanner.scan_all(target_ns)
        logger.info(f"Found {len(resources)} resources")

        # Calculate costs and detect untracked money
        logger.info("Analyzing untracked money...")
        analysis = self.detector.analyze_all(resources)

        # Generate summary report
        report = self.analyzer.generate_summary_report(analysis)
        print("\n" + "=" * 80)
        print(report)
        print("=" * 80 + "\n")

        # Get high-impact violations
        threshold = self.config.get('min_cost_threshold', 1.0)
        violations = self.detector.get_high_impact_violations(resources, threshold)
        logger.info(f"Found {len(violations)} high-impact violations")

        # Analyze with AI
        if violations:
            logger.info("Getting AI recommendations...")
            ai_results = []
            for untracked in violations:
                recommendation = self.analyzer.analyze_resource(
                    untracked.resource,
                    untracked
                )
                ai_results.append((untracked.resource, untracked, recommendation))

            # Create GitHub issues
            dry_run = self.config.get('dry_run', False)
            if dry_run:
                logger.info("[DRY RUN] Would create issues for violations")

            logger.info("Creating GitHub issues...")
            results = self.github.create_issues_batch(ai_results, dry_run)

            logger.info(f"Issues created: {len(results['created'])}")
            logger.info(f"Duplicates skipped: {len(results['duplicates'])}")
            logger.info(f"Failed: {len(results['failed'])}")

            return {
                'analysis': analysis,
                'violations': len(violations),
                'issues_created': len(results['created']),
                'report': report
            }

        return {
            'analysis': analysis,
            'violations': 0,
            'issues_created': 0,
            'report': report
        }


def load_config() -> dict:
    """Load configuration from environment."""
    # Load .env file if it exists
    env_path = Path('.env')
    if env_path.exists():
        load_dotenv()

    return {
        'kubeconfig_path': os.getenv('KUBECONFIG_PATH'),
        'target_namespace': os.getenv('TARGET_NAMESPACE'),
        'pricing_config': os.getenv('PRICING_CONFIG'),
        'tagging_rules': os.getenv('TAGGING_RULES'),
        'bedrock_model_id': os.getenv('BEDROCK_MODEL_ID'),
        'aws_region': os.getenv('AWS_REGION', 'us-east-1'),
        'github_token': os.getenv('GITHUB_TOKEN'),
        'github_repo': os.getenv('GITHUB_REPO'),
        'log_level': os.getenv('LOG_LEVEL', 'INFO'),
        'dry_run': os.getenv('DRY_RUN', 'false').lower() == 'true',
        'min_cost_threshold': float(os.getenv('MIN_COST_THRESHOLD', '1.0')),
        'use_mock': os.getenv('USE_MOCK', 'false').lower() == 'true',
        'use_mock_github': os.getenv('USE_MOCK_GITHUB', 'false').lower() == 'true',
    }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='K8s FinOps Agent')
    parser.add_argument('--kubeconfig', help='Path to kubeconfig file')
    parser.add_argument('--namespace', '-n', help='Target namespace')
    parser.add_argument('--dry-run', '-d', action='store_true', help='Dry run mode')
    parser.add_argument('--mock', '-m', action='store_true', help='Use mock analyzer')
    parser.add_argument('--mock-github', action='store_true', help='Use mock GitHub client')
    parser.add_argument('--threshold', '-t', type=float, default=1.0, help='Minimum cost threshold')
    parser.add_argument('--log-level', '-l', default='INFO', help='Log level')

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)

    logger.info("Starting K8s FinOps Agent")

    # Load configuration
    config = load_config()

    # Override with command line args
    if args.kubeconfig:
        config['kubeconfig_path'] = args.kubeconfig
    if args.namespace:
        config['target_namespace'] = args.namespace
    if args.dry_run:
        config['dry_run'] = True
    if args.mock:
        config['use_mock'] = True
    if args.mock_github:
        config['use_mock_github'] = True
    if args.threshold:
        config['min_cost_threshold'] = args.threshold

    # Initialize and run agent
    agent = FinOpsAgent(config)
    if not agent.initialize():
        logger.error("Failed to initialize agent")
        sys.exit(1)

    try:
        results = agent.run_scan()
        logger.info("FinOps scan completed successfully")
        logger.info(f"Total untracked: ${results['analysis']['total_untracked']}/month")
        logger.info(f"Issues created: {results['issues_created']}")
    except Exception as e:
        logger.error(f"Scan failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
